
textList = [
  "park's",
  "residential complex's",
  "campus'",
  "resort's",
  "hotel's",
];

const cycle = document.querySelector("#changing-text");
const biodiversity = document.querySelector("#biodiversity");

let i = 0;
const cycleText = () => {

    

    cycle.className = "fadeOut";
    biodiversity.className = "fadeOut";

    // will fade in after 1.5s = length of fadeout animation
    setTimeout(function () {
    cycle.className = "";
    cycle.className = "fadeIn";

    biodiversity.className = "";
    biodiversity.className = "fadeIn";

    cycle.innerHTML = ""; biodiversity.innerHTML = "";

    cycle.innerHTML = textList[i];
    biodiversity.innerHTML = " biodiversity";
  }, 1600);

  i = ++i % textList.length;
};

// cycle.className = "fadeIn";
// biodiversity.className = "fadeIn";
// cycle.innerHTML = textList[i];
// biodiversity.innerHTML = "biodiversity";


setInterval(cycleText, 4000);
