
textList = [
  "park",
    "residential complex",

  "college",
  "campus",
  "resort",
  "hotel",
  "school",

  
];

const cycle = document.querySelector("#changing-text");

let i = 0;
const cycleText = () => {



    cycle.className = "fadeOut";

    // will fade in after 1.5s = length of fadeout animation
    setTimeout(function () {
    cycle.className = "";
    cycle.className = "fadeIn";


    cycle.innerHTML = ""; 

    cycle.innerHTML = textList[i];
  }, 500);

  i = ++i % textList.length;
};

// cycle.className = "fadeIn";
// biodiversity.className = "fadeIn";
// cycle.innerHTML = textList[i];
// biodiversity.innerHTML = "biodiversity";
setTimeout(function () {
    cycleText.call();

}, 1000)

setTimeout(function() {
    setInterval(cycleText, 2000);
}, 1000)


