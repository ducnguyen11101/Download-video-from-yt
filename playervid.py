#đã thêm thanh âm lượng, khá ổn
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys

class Window(QWidget):
    def __init__(self):# tạo cửa số phát video
        super().__init__()

        self.setWindowIcon(QIcon("player.ico"))
        self.setWindowTitle("PyPlayer")
        self.setGeometry(350, 100, 700, 500)

        # p = self.palette()
        # light_blue_color = QColor(173, 216, 230)
        # p.setColor(QPalette.Window, light_blue_color)
        # self.setPalette(p)

        self.create_player()
        
    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()
        # nút mở file
        self.openBtn = QPushButton('Open Your Video Here')
        self.openBtn.clicked.connect(self.open_file)

        # nút play
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # nút âm lượng
        self.volumeBtn = QPushButton()
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.setToolTip("Volume")
        self.volumeBtn.setCheckable(True)
        self.volumeBtn.clicked.connect(self.toggle_volume_slider)

        # thanh âm lượng
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setValue(50)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setToolTip("Volume")
        self.volumeSlider.setVisible(False)
        self.volumeSlider.setFixedWidth(100)
        self.volumeSlider.valueChanged.connect(self.change_volume)

        # thanh trượt video
        self.videoSlider = QSlider(Qt.Horizontal)
        self.videoSlider.setValue(0)
        self.videoSlider.setToolTip("Position")
        self.videoSlider.sliderMoved.connect(self.set_position)

        self.zoomBtn = QPushButton()
        self.zoomBtn.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.zoomBtn.clicked.connect(self.zoom_video)

        hbox1 = QHBoxLayout()
        # hbox.setContentsMargins(50,0,0,0)
        hbox1.addWidget(self.videoSlider)

        hbox = QHBoxLayout()
        # hbox.setContentsMargins(50,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.volumeBtn)
        hbox.addWidget(self.volumeSlider)
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hbox.addItem(spacer)
        hbox.addWidget(self.zoomBtn)

        # hbox.addWidget(self.videoSlider)

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox)

        self.mediaPlayer.setVideoOutput(videowidget)
        self.setLayout(vbox)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):# phát/dừng video
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def zoom_video(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())