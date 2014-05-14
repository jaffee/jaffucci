var target_date = new Date(2014, 8, 13, 17, 0, 0, 0);
console.log(target_date);
var now = new Date();

var count = Math.round((target_date - now) / 1000);
console.log(count);


var counter=setInterval(timer, 1000); //1000 will  run it every 1 second

function timer()
{
  count = count-1;
  seconds_per_day = 24*60*60;
  seconds_per_hour = 60*60;
  var days = Math.floor(count/seconds_per_day);
  var hours = Math.floor((count - (days*seconds_per_day))/seconds_per_hour);
  var minutes = Math.floor((count - (days*seconds_per_day) - (hours*seconds_per_hour))/60);
  var seconds = Math.floor(count - (days*seconds_per_day) - (hours*seconds_per_hour) - minutes*60);
  $("#days").text(Math.round(days));
  $("#hours").text(Math.round(hours));
  $("#minutes").text(Math.round(minutes));
  $("#seconds").text(Math.round(seconds));
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
