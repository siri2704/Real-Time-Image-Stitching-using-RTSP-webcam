# Real-Time-Image-Stitching-using-RTSP-webcam
 RTSP Stream and Image Stitching

This project demonstrates how to capture video from RTSP streams, process the frames, and stitch two images together using OpenCV.

## Features

- Connects to two RTSP streams.
- Captures and resizes frames from the streams.
- Stitches the frames together to create a panoramic view.
- Reconnects automatically if the connection fails.

## Requirements

- Python 3.x
- OpenCV
- NumPy

You can install the required Python packages using `pip`:

```bash
pip install numpy opencv-python imutils
Usage
Clone the repository:

bash
Copy code
git clone https://github.com/siri2704/your-repository-name.git
Navigate to the project directory:

bash
Copy code
cd your-repository-name
Edit the source URLs:

Open the main.py file and replace the source1 and source2 URLs with your RTSP stream URLs.

python
Copy code
source1 = "rtsp://<your_ip>:<port>/ch01.264" 
source2 = "rtsp://<your_ip>:<port>/ch01.264"
Run the script:

bash
Copy code
python main.py
Exit the program:

Press 'q' while the program window is focused to exit.

Troubleshooting
Error: Cannot open video source: Ensure that the RTSP stream URLs are correct and accessible.
Stitching failed or produced no valid result: Verify that both streams are correctly connected and are providing frames.

Contributing
Feel free to submit issues and pull requests. If you have suggestions for improvements or additional features, please open an issue to discuss it.
