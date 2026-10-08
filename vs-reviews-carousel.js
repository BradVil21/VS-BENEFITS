/* VS Health Benefits review carousel (shared by every page with a "What clients say" section).
   To add a review: put a new entry at the TOP of the list below. That's the only edit needed;
   the "from N Google reviews" badge is updated separately (or live by /vs-reviews.js). */
(function(){
  var reviews=[
     {
      "name": "Ashley S.",
      "initials": "AS",
      "color": "#0db5a6",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "I had a great experience getting my health insurance! The process was smooth, stress-free, and easy to understand. Everything was explained clearly, and I felt confident choosing a plan that fit my needs and budget. Excellent customer service, very professional, and genuinely helpful. Highly recommend to anyone looking for affordable, reliable health coverage!"
     },
     {
      "name": "Nick D.",
      "initials": "ND",
      "color": "#16447f",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "Great experience! My agent took the time to explain my health insurance options clearly and answer all my questions without making me feel rushed or pressured. I felt supported throughout the process and more confident choosing my coverage. Highly recommend!"
     },
     {
      "name": "Jordan R.",
      "initials": "JR",
      "color": "#16447f",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley is such a caring person, he didn’t only help my mom find an amazing option, but then helped me find an option even though my schedule is crazy and I get home from work at 9:30pm every night. Thank you Brad!!"
     },
     {
      "name": "Selah H.",
      "initials": "SH",
      "color": "#0db5a6",
      "role": "First-time buyer",
      "date": "Google review",
      "stars": 5,
      "text": "Brad has been the BEST in helping me , sharing information, and being in the loop with my insurance. I genuinely couldn’t have asked for anyone better and will be only using him in the future ! Amazing costumer service , beyond expectations. I’m 25 and not very educated or experienced with insurance and he made everything so clear and understandable. Outstanding truly."
     },
     {
      "name": "Chloe B.",
      "initials": "CB",
      "color": "#1e5ab0",
      "role": "Small business owner",
      "date": "Google review",
      "stars": 5,
      "text": "I worked with Brad when I was looking for insurance for my small business. He was great! He showed me several different plans and explained everything in simple terms. We got a great plan with bcbs that we’re very happy with. 10/10 great service and I would recommend him."
     },
     {
      "name": "Gabrielle F.",
      "initials": "GF",
      "color": "#098374",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "Absolutely an amazing experience! Brad was the best agent I have ever worked with. Not only is he super kind but made sure to put me on the best plan possible that fits my situation. 10/10 would recommend!"
     },
     {
      "name": "Kimberly P.",
      "initials": "KP",
      "color": "#2f7de0",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley is genuinely one of the most helpful and supportive people I’ve talk to on the phone. He genuinely cared to help me with my situation, and I’m beyond thankful because he gave me lots of support and encouragement to help find the perfect insurance for me, which I was in great need of."
     },
     {
      "name": "Sinai E.",
      "initials": "SE",
      "color": "#16447f",
      "role": "Family plan",
      "date": "Google review",
      "stars": 5,
      "text": "Brad was the friendliest, most helpful advisor! He matched my family and I with a great coverage plan that fits all of our needs. Will definitely keep him close for any future needs!"
     },
     {
      "name": "Julian R.",
      "initials": "JR",
      "color": "#0db5a6",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "I can’t recommend Bradley enough for anyone feeling overwhelmed by health insurance options. From the very first conversation, he took the time to actually listen to my specific needs and budget rather than just pushing a standard plan. What I appreciated most was his ability to break down complex terms into plain English, ensuring I understood exactly what my coverage included and what it didn’t. He made the entire process seamless, efficient, and stress-free. If you’re looking for a professional who combines deep industry knowledge with a genuine client first attitude, Bradley is your guy!"
     },
     {
      "name": "Rebekah C.",
      "initials": "RC",
      "color": "#1e5ab0",
      "role": "New to health insurance",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley was very helpful, especially for someone like me who’s new to health insurance. He explained everything clearly and made the process feel easy and stress-free."
     },
     {
      "name": "Ross P.",
      "initials": "RP",
      "color": "#098374",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "I had a great experience with VS Health Benefits. I worked with Bradley and Jake and they were both extremely friendly and helpful and made the entire process so much less stressful and easier than I thought it was going to be. We went over what I needed and 10 minutes later they had me set up with the perfect plan for me and it costs way less than I was expecting. I specifically appreciate how Jake explained exactly what I was getting and what it meant, he made it very simple and easy to understand. I highly recommend VS Health Benefits for anyone looking for affordable personalized healthcare coverage!!"
     },
     {
      "name": "Edwin M.",
      "initials": "EM",
      "color": "#2f7de0",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "I had an amazing experience working with Bradley! His professionalism, patience, and extensive knowledge of health insurance made the entire process smooth and stress-free. He took the time to explain all my options clearly and helped me choose the best plan for my needs and budget. Bradley truly cares about helping his clients and made me feel confident in my decision every step of the way. I’m incredibly grateful for his guidance and support. Thank you so much, Bradley, for your outstanding service — highly recommend!"
     },
     {
      "name": "Alex D.",
      "initials": "AD",
      "color": "#16447f",
      "role": "Family plan",
      "date": "Google review",
      "stars": 5,
      "text": "Mr. Bradley was excellent with his communication and service, really helped my family out find the best option we'd had seen on the market!"
     },
     {
      "name": "Lesley Ann L.",
      "initials": "LL",
      "color": "#0db5a6",
      "role": "Individual coverage",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley was informative, helpful and professional. He educated me on all my options and was able to secure health insurance. I recommend them to everyone"
     },
     {
      "name": "Carolyn F.",
      "initials": "CF",
      "color": "#1e5ab0",
      "role": "Bilingual service",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley provided an exceptional level of customer service that truly distinguished him from the rest. His professionalism, attentiveness, and ability to create such a comforting yet informative experience were genuinely impressive. He was articulate, patient, and incredibly knowledgeable, ensuring I felt supported and well-informed throughout every interaction. His bilingual communication skills made the experience even more seamless and welcoming, further reflecting his dedication to providing outstanding service to everyone he assists. Bradley carries himself with remarkable professionalism and grace, and it is evident that he genuinely cares about the people he helps, he exceeded expectations and left a lasting impression. An absolute asset to the team and truly exceptional at what he does."
     },
     {
      "name": "Logan M.",
      "initials": "LM",
      "color": "#098374",
      "role": "Client",
      "date": "Google review",
      "stars": 5,
      "text": "Owner gave me a lot of incredibly helpful advice, was very patient explained in detail the process of this business and made me understand what to look for when looking into this. Bradley is a phenomenal individual that I would recommend close family and friends to."
     },
     {
      "name": "Gustavo V.",
      "initials": "GV",
      "color": "#2f7de0",
      "role": "Client",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley was very helpful, professional, and easy to work with. He answered all my questions and made the process simple. I highly recommend him if you’re looking for health insurance!"
     },
     {
      "name": "Savannah D.",
      "initials": "SD",
      "color": "#16447f",
      "role": "Client",
      "date": "Google review",
      "stars": 5,
      "text": "Bradley was very helpful and professional and made sure I understood everything without making me feel silly."
     },
     {
      "name": "Estrella G.",
      "initials": "EG",
      "color": "#0db5a6",
      "role": "Client",
      "date": "Google review",
      "stars": 5,
      "text": "10/10 Bradley was fast, efficient and got me exactly what I needed. Thank you so much! Definitely and HIGHLY recommend."
     }
    ];
  function stars(n){return "\u2605".repeat(n)+"\u2606".repeat(5-n);}
  function gIcon(){return '<svg width="14" height="14" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.29-8.16 2.29-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>';}
  function card(r){
    return '<div class="rcard"><div class="rcard-top"><div class="rcard-who">'
      +'<div class="rcard-avatar" style="background:'+r.color+'">'+r.initials+'</div>'
      +'<div><div class="rcard-name">'+r.name+'</div><div class="rcard-meta">'+r.role+' &middot; '+r.date+'</div></div>'
      +'</div><div class="rcard-stars">'+stars(r.stars)+'</div></div>'
      +'<div class="rcard-text">'+r.text+'</div>'
      +'<div class="rcard-foot">'+gIcon()+'<span>Google Review</span></div></div>';
  }
  if(!document.getElementById('vs-rcard-css')){
    var st=document.createElement('style');st.id='vs-rcard-css';
    st.textContent="#reviews-track:hover{animation-play-state:paused}\n.rcard-text{display:-webkit-box;-webkit-line-clamp:8;-webkit-box-orient:vertical;overflow:hidden}\n@keyframes reviewScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}\n.rcard{flex:0 0 320px;background:#fff;border:1px solid var(--line,#e4e9f2);border-radius:16px;padding:22px;display:flex;flex-direction:column;gap:12px;transition:transform .25s var(--ease,cubic-bezier(.2,.7,.2,1)),box-shadow .25s var(--ease,cubic-bezier(.2,.7,.2,1)),border-color .2s;cursor:default}\n.rcard:hover{transform:translateY(-3px);box-shadow:var(--shadow,0 10px 30px rgba(13,27,42,.10));border-color:var(--blue-100,#e8f0fb)}\n.rcard-top{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}\n.rcard-who{display:flex;align-items:center;gap:10px}\n.rcard-avatar{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.88rem;color:#fff;flex-shrink:0}\n.rcard-name{font-weight:700;font-size:.93rem;color:var(--ink,#0d1b2a);line-height:1.2}\n.rcard-meta{font-size:.76rem;color:var(--muted,#5a6b80);margin-top:2px}\n.rcard-stars{color:#FBBC05;font-size:.98rem;letter-spacing:1px}\n.rcard-text{font-size:.9rem;color:var(--ink-2,#334155);line-height:1.65;font-style:italic}\n.rcard-text::before{content:'\\201C';font-size:1.35rem;color:var(--blue-500,#2f7de0);line-height:0;vertical-align:-.3em;margin-right:1px}\n.rcard-text::after{content:'\\201D';font-size:1.35rem;color:var(--blue-500,#2f7de0);line-height:0;vertical-align:-.3em;margin-left:1px}\n.rcard-foot{display:flex;align-items:center;gap:5px;margin-top:auto;opacity:.55}\n.rcard-foot span{font-size:.76rem;font-weight:600;color:var(--muted,#5a6b80)}\n@media(max-width:640px){.rcard{flex:0 0 270px}}";
    (document.head||document.documentElement).appendChild(st);
  }
  function render(){
    var track=document.getElementById('reviews-track');
    if(!track||track.getAttribute('data-done'))return;
    track.innerHTML=reviews.concat(reviews).map(card).join('');
    track.setAttribute('data-done','1');
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',render);else render();
})();
