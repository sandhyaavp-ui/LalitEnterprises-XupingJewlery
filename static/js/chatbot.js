/* ==========================================================================
   Xuping Jewellery — rule-based chat widget (no API key, no external calls
   except submitting an enquiry to the site's own Django backend).
   Covers: FAQs, browsing collections, and taking an enquiry.
   ========================================================================== */

(function () {
  var WHATSAPP_URL = 'https://wa.me/919841066880';

  var COLLECTIONS = [
    { name: 'Bali', url: '/collection/bali/' },
    { name: 'Stud', url: '/collection/stud/' },
    { name: 'Pendant Chain', url: '/collection/pendant-chain/' },
    { name: 'Chain', url: '/collection/chain/' },
    { name: 'Ring', url: '/collection/ring/' },
    { name: 'Kada', url: '/collection/kada/' },
    { name: 'Bracelet', url: '/collection/bracelet/' },
    { name: 'Adjustable Bracelet', url: '/collection/adjustable-bracelet/' }
  ];

  var FAQS = [
    {
      q: 'Minimum order quantity & amount',
      keywords: ['moq', 'minimum', 'quantity', 'amount', 'mop'],
      a: 'Our standard minimum is 6 pieces per design for Bali, Stud and Bracelet collections. For Kada, Ring, Chain, Pendant Chain and Adjustable Bracelet, the minimum is 2 pieces per design. Across all designs combined, your total order must add up to at least ₹20,000.'
    },
    {
      q: 'How do I place an order?',
      keywords: ['order', 'place', 'how to buy'],
      a: 'Browse our Everyday Collections, then message us on WhatsApp or book a video call for live pricing. Once finalised, confirm and pay, and we pack and ship it.'
    },
    {
      q: 'Payment methods',
      keywords: ['payment', 'pay', ' upi', 'bank transfer'],
      a: 'We accept UPI (Google Pay, PhonePe, any UPI app), direct bank transfer, or WhatsApp Pay. Details are shared once your order is finalised.'
    },
    {
      q: 'Dispatch & delivery time',
      keywords: ['dispatch', 'delivery', 'shipping', 'ship', 'how long'],
      a: 'Once confirmed and paid, we pack and ship from Chennai within 24–48 hours. Delivery time after that depends on your location in India.'
    },
    {
      q: 'Do you ship pan-India?',
      keywords: ['pan-india', 'ship india', 'which cities', 'state'],
      a: 'Yes — we ship to resellers, boutique owners and retailers anywhere in India.'
    },
    {
      q: 'Can I see products on a video call first?',
      keywords: ['video call', 'see products', 'live', 'camera'],
      a: 'Yes, and we recommend it! Book a free 1-on-1 video call and we’ll show you the actual pieces live — finish, colour, weight and size — before you order.'
    },
    {
      q: 'Your store address',
      keywords: ['address', 'location', 'where are you', 'shop location', 'visit', 'directions'],
      a: 'We’re located at 39/2 EK, Agraharam St, Edapalaiyam, Park Town, Chennai, Tamil Nadu 600003. <a href="https://www.google.com/maps/search/?api=1&query=Xuping+Jewelery+India+agent+LALIT+ENTERPRISES&query_place_id=ChIJnek5oFdvUjoRz5JeDE9KjXg" target="_blank" rel="noopener">Open in Google Maps</a>.'
    },
    {
      q: 'Contact phone number',
      keywords: ['phone', 'number', 'contact number', 'mobile', 'call you'],
      a: 'You can reach us at 098410 66880 — this number works for calls, WhatsApp, and general enquiries, Monday to Saturday, 11:00 AM to 6:00 PM.'
    },
    {
      q: 'Are you an authorised agent?',
      keywords: ['authorised', 'authorized', 'genuine agent', 'official agent', 'certified'],
      a: 'Yes — we are an authorised Xuping wholesale agent based in Chennai, so every piece you order through us is genuine and traceable.'
    },
    {
      q: 'Do you only sell Xuping products?',
      keywords: ['only xuping', 'other brands', 'xuping only', 'just xuping', 'exclusively xuping'],
      a: 'Yes — our entire collection is exclusively Xuping jewellery. We don’t stock or mix in any other brand, so you can be confident every design you see here is genuine Xuping stock.'
    },
    {
      q: 'How often do you add new designs?',
      keywords: ['new designs', 'how often', 'new styles', 'monthly', 'restock', 'fresh designs'],
      a: 'We refresh our collection every month with new Xuping styles. Keep your store current and your customers engaged with fresh options.'
    }
  ];

  var state = 'menu';
  var enquiry = { name: '', phone: '', message: '' };
  var videoCallState = { full_name: '', phone: '', location: '', date: '', time: '' };
  var TIME_SLOTS = ['11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'];

  function getCookie(name) {
    var match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? match.pop() : '';
  }

  function el(tag, className, text) {
    var e = document.createElement(tag);
    if (className) e.className = className;
    if (text) e.textContent = text;
    return e;
  }

  function addMessage(text, from) {
    var body = document.getElementById('xj-chat-body');
    var msg = document.createElement('div');
    msg.className = 'xj-msg xj-msg-' + from;
    if (from === 'bot') {
      // Bot messages are all hardcoded above (FAQS, static strings) — never
      // user input — so innerHTML is safe here and lets the address FAQ's
      // <a> link render as a clickable link instead of literal text.
      msg.innerHTML = text;
    } else {
      // User-typed text goes through textContent always, since this is
      // raw user input and must never be interpreted as HTML.
      msg.textContent = text;
    }
    body.appendChild(msg);
    body.scrollTop = body.scrollHeight;
  }

  function addQuickReplies(options) {
    var body = document.getElementById('xj-chat-body');
    var wrap = el('div', 'xj-quick-replies');
    options.forEach(function (opt) {
      var btn = el('button', 'xj-quick-btn', opt.label);
      btn.type = 'button';
      btn.addEventListener('click', opt.onClick);
      wrap.appendChild(btn);
    });
    body.appendChild(wrap);
    body.scrollTop = body.scrollHeight;
  }

  function showMenu() {
    state = 'menu';
    addMessage('What would you like to do?', 'bot');
    addQuickReplies([
      { label: 'Browse collections', onClick: showCollections },
      { label: 'Ask a question', onClick: showFaqMenu },
      { label: 'Book a video call', onClick: startVideoCallBooking },
      { label: 'Leave an enquiry', onClick: startEnquiry },
      { label: 'Chat on WhatsApp', onClick: function () { window.open(WHATSAPP_URL, '_blank'); } }
    ]);
  }

  function showCollections() {
    state = 'collections';
    addMessage('Here’s our Everyday Collection — tap one to view designs:', 'bot');
    var opts = COLLECTIONS.map(function (c) {
      return { label: c.name, onClick: function () { window.location.href = c.url; } };
    });
    opts.push({ label: '← Back', onClick: showMenu });
    addQuickReplies(opts);
  }

  function showFaqMenu() {
    state = 'faq';
    addMessage('Pick a question:', 'bot');
    var opts = FAQS.map(function (f) {
      return { label: f.q, onClick: function () { addMessage(f.q, 'user'); addMessage(f.a, 'bot'); showFaqFollowUp(); } };
    });
    opts.push({ label: '← Back', onClick: showMenu });
    addQuickReplies(opts);
  }

  function showFaqFollowUp() {
    addQuickReplies([
      { label: 'Another question', onClick: showFaqMenu },
      { label: 'Main menu', onClick: showMenu }
    ]);
  }

  function startEnquiry() {
    state = 'enquiry-name';
    enquiry = { name: '', phone: '', message: '' };
    addMessage('Sure — what’s your name?', 'bot');
  }

  function submitEnquiry() {
    addMessage('Sending your enquiry…', 'bot');
    fetch('/chatbot/enquiry/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(enquiry)
    })
      .then(function (res) { return res.ok ? res.json() : Promise.reject(); })
      .then(function () {
        addMessage('Thanks, ' + enquiry.name + '! We reply the same working day. For the fastest response, message us on WhatsApp.', 'bot');
        addQuickReplies([
          { label: 'WhatsApp us', onClick: function () { window.open(WHATSAPP_URL, '_blank'); } },
          { label: 'Main menu', onClick: showMenu }
        ]);
      })
      .catch(function () {
        addMessage('Sorry, something went wrong sending that. Please WhatsApp us instead — it’s the fastest way to reach us.', 'bot');
        addQuickReplies([
          { label: 'WhatsApp us', onClick: function () { window.open(WHATSAPP_URL, '_blank'); } },
          { label: 'Main menu', onClick: showMenu }
        ]);
      });
    state = 'menu';
  }

  function startVideoCallBooking() {
    state = 'vc-name';
    videoCallState = { full_name: '', phone: '', location: '', date: '', time: '' };
    addMessage('Sure — let’s get your video call booked. What’s your full name?', 'bot');
  }

  function submitVideoCallBooking() {
    addMessage('Booking your call…', 'bot');
    fetch('/video-call/book/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(videoCallState)
    })
      .then(function (res) { return res.ok ? res.json() : Promise.reject(); })
      .then(function () {
        addMessage('You’re booked in, ' + videoCallState.full_name + '! We’ll confirm by phone. You can also see this under "Your calls" on the Book a Video Call page.', 'bot');
        showMenu();
      })
      .catch(function () {
        addMessage('Something went wrong booking that. Want to try the full booking page instead, or WhatsApp us directly?', 'bot');
        addQuickReplies([
          { label: 'Go to booking page', onClick: function () { window.location.href = '/video-call/'; } },
          { label: 'WhatsApp us', onClick: function () { window.open(WHATSAPP_URL, '_blank'); } },
          { label: 'Main menu', onClick: showMenu }
        ]);
      });
    state = 'menu';
  }

  function matchFaq(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < FAQS.length; i++) {
      for (var j = 0; j < FAQS[i].keywords.length; j++) {
        if (lower.indexOf(FAQS[i].keywords[j]) !== -1) return FAQS[i];
      }
    }
    return null;
  }

  function matchCollection(text) {
    var lower = text.toLowerCase();
    for (var i = 0; i < COLLECTIONS.length; i++) {
      if (lower.indexOf(COLLECTIONS[i].name.toLowerCase()) !== -1) return COLLECTIONS[i];
    }
    return null;
  }

  function handleFreeText(text) {
    addMessage(text, 'user');

    if (state === 'enquiry-name') {
      enquiry.name = text;
      state = 'enquiry-phone';
      addMessage('Thanks! What’s the best phone number to reach you on?', 'bot');
      return;
    }
    if (state === 'enquiry-phone') {
      enquiry.phone = text;
      state = 'enquiry-message';
      addMessage('Got it. What would you like to ask or order?', 'bot');
      return;
    }
    if (state === 'enquiry-message') {
      enquiry.message = text;
      submitEnquiry();
      return;
    }

    if (state === 'vc-name') {
      videoCallState.full_name = text;
      state = 'vc-phone';
      addMessage('Thanks! What’s the best phone number to reach you on? (10 digits)', 'bot');
      return;
    }
    if (state === 'vc-phone') {
      var digitsOnly = text.replace(/\D/g, '');
      if (digitsOnly.length !== 10) {
        addMessage('That doesn’t look like a 10-digit number — could you re-enter it?', 'bot');
        return;
      }
      videoCallState.phone = digitsOnly;
      state = 'vc-location';
      addMessage('Got it. What city/state are you in? (e.g. Chennai - Tamil Nadu)', 'bot');
      return;
    }
    if (state === 'vc-location') {
      videoCallState.location = text;
      state = 'vc-date';
      addMessage('What date works for you? (please type as DD-MM-YYYY, must be a future date)', 'bot');
      return;
    }
    if (state === 'vc-date') {
      // Expects DD-MM-YYYY, converts to YYYY-MM-DD for the backend.
      // Checks each part is actually numeric (not just "3 things split by
      // hyphens" — "not-a-date" also splits into 3 parts) and forms a real
      // calendar date (catches things like 31-02-2026) before checking it's
      // in the future.
      var parts = text.split('-');
      var dayStr = parts[0], monthStr = parts[1], yearStr = parts[2];
      var numericFormat = parts.length === 3
        && /^\d{1,2}$/.test(dayStr)
        && /^\d{1,2}$/.test(monthStr)
        && /^\d{4}$/.test(yearStr);
      if (!numericFormat) {
        addMessage('Please enter the date as DD-MM-YYYY, e.g. 25-12-2026.', 'bot');
        return;
      }
      var day = parseInt(dayStr, 10);
      var month = parseInt(monthStr, 10);
      var year = parseInt(yearStr, 10);
      var dateObj = new Date(year, month - 1, day);
      var isRealCalendarDate = dateObj.getFullYear() === year && dateObj.getMonth() === month - 1 && dateObj.getDate() === day;
      if (!isRealCalendarDate) {
        addMessage('That doesn’t look like a real date — please enter DD-MM-YYYY, e.g. 25-12-2026.', 'bot');
        return;
      }
      var isoDate = yearStr + '-' + monthStr.padStart(2, '0') + '-' + dayStr.padStart(2, '0');
      var today = new Date().toISOString().split('T')[0];
      if (isoDate <= today) {
        addMessage('Please choose a future date.', 'bot');
        return;
      }
      videoCallState.date = isoDate;
      state = 'vc-time';
      addMessage('And what time works best?', 'bot');
      addQuickReplies(TIME_SLOTS.map(function (slot) {
        return { label: slot, onClick: function () {
          addMessage(slot, 'user');
          videoCallState.time = slot;
          addMessage('Great — confirming your booking now.', 'bot');
          submitVideoCallBooking();
        }};
      }));
      return;
    }

    var faq = matchFaq(text);
    if (faq) {
      addMessage(faq.a, 'bot');
      showFaqFollowUp();
      return;
    }
    var collection = matchCollection(text);
    if (collection) {
      addMessage('Here you go — our ' + collection.name + ' designs:', 'bot');
      addQuickReplies([
        { label: 'View ' + collection.name, onClick: function () { window.location.href = collection.url; } },
        { label: 'Main menu', onClick: showMenu }
      ]);
      return;
    }

    addMessage('I’m not sure about that one — want to ask our team directly on WhatsApp, or see the menu again?', 'bot');
    addQuickReplies([
      { label: 'WhatsApp us', onClick: function () { window.open(WHATSAPP_URL, '_blank'); } },
      { label: 'Main menu', onClick: showMenu }
    ]);
  }

  function initWidget() {
    var launcher = document.getElementById('xj-chat-launcher');
    var panel = document.getElementById('xj-chat-panel');
    var closeBtn = document.getElementById('xj-chat-close');
    var form = document.getElementById('xj-chat-form');
    var input = document.getElementById('xj-chat-input');
    var opened = false;

    launcher.addEventListener('click', function () {
      panel.classList.toggle('is-open');
      if (!opened) {
        opened = true;
        addMessage('Hi! I’m the Lalit Enterprises assistant. I can help you browse collections, answer questions, or take your enquiry.', 'bot');
        showMenu();
      }
    });

    closeBtn.addEventListener('click', function () {
      panel.classList.remove('is-open');
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      input.value = '';
      handleFreeText(text);
    });
  }

  document.addEventListener('DOMContentLoaded', initWidget);
})();
