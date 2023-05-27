function openVideoModal(videoSrc) {
    var videoPlayer = document.getElementById('video-player');
    videoPlayer.src = videoSrc;
    $('#video-player-modal').modal('show');
}

function downloadFootage(footageName) {
    var link = document.createElement('a');
    link.href = footageName;
    link.download = footageName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}