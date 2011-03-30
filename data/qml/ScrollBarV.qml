/*
	ScrollBar component for QML Flickable

	Copyright (c) 2010 Gregory Schlomoff - gregory.schlomoff@gmail.com

	This code is released under the MIT license

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.
*/

/*
	Usage:

	Flickable {
	  id: myFlickable
	  ...
	}
	ScrollBar {
	  target: myFlickable
	}
*/

import Qt 4.7

BorderImage {
	property variant target

	source: "images/scrollbarv.png"
	border {left: 3; top: 0; right: 3; bottom: 0}
	height: 16

	anchors {left: target.left; right: target.right; bottom: target.bottom; rightMargin: 20 }
	visible: (track.width == slider.width) ? false : true //TODO: !visible -> width: 0 (but creates a binding loop)

	Item {
		anchors {fill: parent; margins: 0; rightMargin: 0; bottomMargin: 0}

		Image {
			id: leArrow
			source: "images/le-arrow.png"
			anchors.left: parent.left
			MouseArea {
				anchors.fill: parent
				onPressed: {
					timer.scrollAmount = -10
					timer.running = true;
				}
				onReleased: {
					timer.running = false;
				}
			}
		}

		Timer {
			property int scrollAmount

			id: timer
			repeat: true
			interval: 20
			onTriggered: {
				target.contentX = Math.max(
						0, Math.min(
						target.contentX + scrollAmount,
						target.contentWidth - target.width));
			}
		}

		Item {
			id: track
			anchors {left: leArrow.right; leftMargin: 1; right: reArrow.left;}
			height: parent.height

			MouseArea {
				anchors.fill: parent
				onPressed: {
					timer.scrollAmount = target.width * (mouseX < slider.x ? -1 : 1)	// scroll by a page
					timer.running = true;
				}
				onReleased: {
					timer.running = false;
				}
			}

			BorderImage {
				id:slider

				source: "images/sliderv.png"
				border {left: 3; top: 0; right: 3; bottom: 0}
				height: parent.height

				width: Math.min(target.width / target.contentWidth * track.width, track.width)
				x: target.visibleArea.xPosition * track.width

				MouseArea {
					anchors.fill: parent
					drag.target: parent
					drag.axis: Drag.YAxis
					drag.minimumX: 0
					drag.maximumX: track.width - width

					onPositionChanged: {
						if (pressedButtons == Qt.UpButton) {
							target.contentX = slider.X * target.contentWidth / track.width
						}
					}
				}
			}
		}
		Image {
			id: reArrow
			source: "images/re-arrow.png"
			anchors.right: parent.right
			//anchors.rightMargin: 17
			MouseArea {
				anchors.fill: parent
				onPressed: {
					timer.scrollAmount = 10
					timer.running = true;
					console.log(track.width);
					console.log(slider.width);
					console.log(target.width);
					console.log(target.contentWidth);
					console.log(target.height);
					console.log(target.contentHeight);
				}
				onReleased: {
					timer.running = false;
				}
			}
		}
	}
}
