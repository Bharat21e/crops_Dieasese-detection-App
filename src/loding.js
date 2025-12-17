import gsap from 'gsap';

export function animateLoadingText() {
  const loding = document.querySelector(".loding");
  if (!loding) return;

  const text = loding.textContent.trim(); // should be "........"
  loding.innerHTML = text
    .split("")
    .map((char) => `<span>${char}</span>`)
    .join("");

  gsap.from( ".loding span",{
     opacity: 0 ,
      duration: 0.6,
      stagger: 0.1,
      repeat: -1
   
  }
  );
}
