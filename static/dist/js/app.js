var region = 'riks';

function updateResult () {
  r = Math.random().toString(36).substring(7);
  $(".live-img").attr("src","getResult?region=" + region + "&time=" + r);
}

function setRegion(reg) {
  if(reg == 'riks') {
    $(".res-header").html("Current results for: Riksdag (Hela Sverige)");
  }
  else if(reg == 'riksSturk') {
    $(".res-header").html("Current results for: Riksdag (Sturkö)");
  }
  else if(reg == 'kommSturk') {
    $(".res-header").html("Current results for: Kommunal (Sturkö)");
  }
  else if(reg == 'kommGbg') {
    $(".res-header").html("Current results for: Kommunal (Göteborg)");
  }
  region = reg;
  updateResult();
}

window.setInterval(function timeFunc () {
  updateResult();
}, 10000);

// Set the inital result header
$(".res-header").html("Current results for: Riksdag (Hela Sverige)");

