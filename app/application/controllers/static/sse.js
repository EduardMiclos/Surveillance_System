// source.onmessage = function(event) {
//   console.log(123123)
//   var data = JSON.parse(event.data);
//   if (data.type === 'refresh' && data.channel === 'admin_updates') {
//     location.reload();
//   }
// };

var source = new EventSource("/stream");
source.addEventListener('camera_register_refresh', _ => {
    location.reload();
}, false);