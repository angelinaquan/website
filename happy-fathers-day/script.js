const fortunes = [
  "愿爸爸身体硬朗，万事胜意。",
  "愿爸爸远离烦恼，常有好心情。",
  "愿爸爸财运福运都在线。",
  "愿爸爸平安喜乐，健康长寿。",
  "愿爸爸所愿皆成，所行皆坦途。",
  "愿爸爸每天都有好茶、好饭、好心情。",
  "愿爸爸睡得香，吃得香。",
  "愿爸爸一路有福气，身边有欢喜。"
];

const intro = document.querySelector("#intro");
const fortuneStage = document.querySelector("#fortuneStage");
const openFortune = document.querySelector("#openFortune");
const redrawFortune = document.querySelector("#redrawFortune");
const fortuneSlip = document.querySelector("#fortuneSlip");
const fortuneText = document.querySelector("#fortuneText");

let previousIndex = -1;

function pickFortune() {
  let nextIndex = Math.floor(Math.random() * fortunes.length);

  if (fortunes.length > 1) {
    while (nextIndex === previousIndex) {
      nextIndex = Math.floor(Math.random() * fortunes.length);
    }
  }

  previousIndex = nextIndex;
  return fortunes[nextIndex];
}

function drawFortune() {
  fortuneSlip.classList.remove("is-changing");
  void fortuneSlip.offsetWidth;
  fortuneSlip.classList.add("is-changing");

  window.setTimeout(() => {
    fortuneText.textContent = pickFortune();
  }, 180);
}

openFortune.addEventListener("click", () => {
  intro.style.display = "none";
  fortuneStage.classList.add("is-visible");
  drawFortune();
});

redrawFortune.addEventListener("click", drawFortune);
