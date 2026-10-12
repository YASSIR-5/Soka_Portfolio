(()=>{const d=document.getElementById('lb');if(!d)return;const i=d.querySelector('img');
document.addEventListener('click',e=>{const a=e.target.closest('a[data-lb]');if(!a)return;e.preventDefault();
i.src=a.href;i.alt=a.querySelector('img').alt;i.classList.remove('z');d.showModal();d.scrollTo(0,0)});
i.addEventListener('click',()=>i.classList.toggle('z'));
d.addEventListener('click',e=>{if(e.target===d||e.target.classList.contains('x'))d.close()})})();
