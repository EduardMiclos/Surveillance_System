var source = new EventSource("/stream");
source.addEventListener('camera_register_refresh', _ => {
    location.reload();
}, false);