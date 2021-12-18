const textarea = document.querySelector('textarea');

textarea.addEventListener('keyup', e =>{
  textarea.style.height = "auto"
  let scHeight = e.target.scrollHeight
  textarea.style.height = `${scHeight}px`

});
