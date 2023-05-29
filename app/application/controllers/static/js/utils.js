function setVideoSource(videoSrc) {
    var videoPlayer = document.getElementById('video-player');
    videoPlayer.src = videoSrc;
}

function downloadFootage(footageName) {
    var link = document.createElement('a');
    link.href = footageName;
    link.download = footageName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}