var source = new EventSource("/stream");

source.addEventListener('CAMERA_REFRESH', _ => {
    location.reload();
}, false);