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

function updateTotalDone () {
  $.get( "getValdistrikt", function( data ) {
      $(".val-title").html("Andreas and Philips Election Results (" + data + ")");
  });
}

window.setInterval(function timeFunc () {
  updateResult();
  // Update number of done
  updateTotalDone();
}, 10000);

// Set the inital result header
$(".res-header").html("Current results for: Riksdag (Hela Sverige)");

// Initial retrival before the timer kicks in
updateResult();
// Update number of done
updateTotalDone();
