#đã thêm thanh âm lượng, khá ổn
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("player.ico"))
        self.setWindowTitle("PyPlayer")
        self.setGeometry(350, 100, 700, 500)

        p = self.palette()
        light_blue_color = QColor(173, 216, 230)
        p.setColor(QPalette.Window, light_blue_color)
        self.setPalette(p)

        self.create_player()

    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        self.openBtn = QPushButton('Open Your Video Here')
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.volumeBtn = QPushButton()
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.setToolTip("Volume")
        self.volumeBtn.setCheckable(True)
        self.volumeBtn.clicked.connect(self.toggle_volume_slider)

        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.setVisible(False)
        self.volumeSlider.valueChanged.connect(self.change_volume)

        self.videoSlider = QSlider(Qt.Horizontal)
        self.videoSlider.setValue(0)
        self.videoSlider.setToolTip("Position")
        self.videoSlider.sliderMoved.connect(self.set_position)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.volumeBtn)
        hbox.addWidget(self.volumeSlider)
        hbox.addWidget(self.videoSlider)

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(videowidget)
        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ =QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.videoSlider.setValue(position)

    def duration_changed(self, duration):
        self.videoSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def toggle_volume_slider(self):
        self.volumeSlider.setVisible(self.volumeBtn.isChecked())

    def change_volume(self, value):
        self.mediaPlayer.setVolume(value)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
