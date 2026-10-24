(function(){
  'use strict';

  // A11y: focus visible
  document.body.classList.add('focus-visible');

  // Nav scroll state
  const nav=document.getElementById('nav');
  if(nav){
    window.addEventListener('scroll',()=>{nav.classList.toggle('scrolled',window.scrollY>40)},{passive:true});
  }

  // Lightbox
  const lb=document.getElementById('lightbox');
  const lbImg=lb?lb.querySelector('img'):null;
  const lbCaption=lb?lb.querySelector('.lb-caption'):null;
  function openLB(src,caption){
    if(!lb||!lbImg)return;
    lbImg.src=src;
    if(lbCaption)lbCaption.textContent=caption||'';
    lb.classList.add('active');
    document.body.style.overflow='hidden';
  }
  function closeLB(){
    if(!lb)return;
    lb.classList.remove('active');
    document.body.style.overflow='';
  }
  if(lb){
    lb.addEventListener('click',(e)=>{if(e.target===lb||e.target.classList.contains('close-btn'))closeLB();});
    document.addEventListener('keydown',(e)=>{if(e.key==='Escape'&&lb.classList.contains('active'))closeLB();});
  }
  document.querySelectorAll('.gallery-card').forEach(c=>{
    c.addEventListener('click',()=>{
      const img=c.querySelector('img');
      const label=c.querySelector('.card-label');
      if(img)openLB(img.src, label?label.textContent:'');
    });
  });

  // Accordion
  document.querySelectorAll('.ac-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const item=btn.closest('.ac-item');
      const wasOpen=item.classList.contains('open');
      document.querySelectorAll('.ac-item').forEach(i=>i.classList.remove('open'));
      if(!wasOpen)item.classList.add('open');
    });
  });

  // Modal contact
  const modal=document.getElementById('modal');
  const openBtn=document.getElementById('open-modal');
  const closeBtn=document.querySelector('.modal-close');
  function openModal(){if(modal)modal.classList.add('active');document.body.style.overflow='hidden';}
  function closeModal(){if(modal)modal.classList.remove('active');document.body.style.overflow='';}
  if(openBtn)openBtn.addEventListener('click',openModal);
  if(closeBtn)closeBtn.addEventListener('click',closeModal);
  if(modal)modal.addEventListener('click',(e)=>{if(e.target===modal)closeModal();});
  document.addEventListener('keydown',(e)=>{if(e.key==='Escape'&&modal&&modal.classList.contains('active'))closeModal();});

  // Contact form: prepare, copy, indicate not sent
  const form=document.getElementById('contact-form');
  const status=document.getElementById('contact-status');
  if(form){
    form.addEventListener('submit',(e)=>{
      e.preventDefault();
      const txt=form.querySelector('textarea').value.trim();
      const name=form.querySelector('input[name="nombre"]').value.trim();
      if(!name||!txt){status.textContent='Completa nombre y mensaje.';status.style.color='var(--amber)';return;}
      const msg='Solicitar presentación — SEDAC\nDe: '+name+'\nMensaje: '+txt+'\nEstado: solicitud preparada; aún no enviada (no hay backend configurado).';
      navigator.clipboard&&navigator.clipboard.writeText(msg).catch(()=>{});
      status.innerHTML='<span style="color:#b0c94d">Solicitud preparada; aún no enviada.</span> <br><span style="font-size:.78rem;color:var(--text-weak)">Copia guardada en portapapeles.</span>';
    });
  }

  // Accordion helper
  window.toggleAc=function(btn){
    const item=btn.closest('.ac-item');
    const open=item.classList.toggle('open');
    btn.setAttribute('aria-expanded', open?'true':'false');
    document.querySelectorAll('.ac-item').forEach(i=>{if(i!==item){i.classList.remove('open');i.querySelector('.ac-btn').setAttribute('aria-expanded','false');}});
  };

  // Mobile nav toggle (optional minimal)
  // Not needed: responsive via CSS but add a mobile menu button if present
  const mobileBtn=document.getElementById('menu-btn');
  const mobilePanel=document.getElementById('mobile-panel');
  if(mobileBtn&&mobilePanel){
    mobileBtn.addEventListener('click',()=>{mobilePanel.classList.toggle('open');});
  }
})();
