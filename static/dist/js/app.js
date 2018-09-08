window.setInterval(function timeFunc () {
  r = Math.random().toString(36).substring(7);
  $(".live-img").attr("src","getResult?region=all&time=" + r);
}, 10000);
