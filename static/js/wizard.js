// 3-step "Book a Video Call" wizard: Your details -> Pick a slot -> Confirmation.
// Submits to /video-call/book/ and then loads /video-call/my-calls/ which the
// backend scopes to the current Django session, so each visitor only ever
// sees their own bookings (see wizard_backend_instructions.md).

(function () {
  var TIME_SLOTS = ['11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'];

  var state = {
    step: 1,
    full_name: '',
    location: '',
    phone: '',
    agreed: false,
    date: '',
    time: ''
  };

  function getCookie(name) {
    var match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? match.pop() : '';
  }

  function goToStep(n) {
    state.step = n;
    document.querySelectorAll('.wizard-panel').forEach(function (p, i) {
      p.classList.toggle('is-active', i === n - 1);
    });
    document.querySelectorAll('.wizard-step').forEach(function (s, i) {
      s.classList.toggle('is-active', i === n - 1);
      s.classList.toggle('is-done', i < n - 1);
    });
    if (n === 3) renderSummary();
  }

  function renderSummary() {
    document.getElementById('wiz-summary-name').textContent = state.full_name;
    document.getElementById('wiz-summary-location').textContent = state.location;
    document.getElementById('wiz-summary-phone').textContent = state.phone;
    document.getElementById('wiz-summary-date').textContent = state.date;
    document.getElementById('wiz-summary-time').textContent = state.time;
  }

  function renderSlots() {
    var grid = document.getElementById('wiz-slot-grid');
    grid.innerHTML = '';
    TIME_SLOTS.forEach(function (slot) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'slot-btn' + (state.time === slot ? ' is-selected' : '');
      btn.textContent = slot;
      btn.addEventListener('click', function () {
        state.time = slot;
        renderSlots();
      });
      grid.appendChild(btn);
    });
  }

  function submitBooking() {
    var submitBtn = document.getElementById('wiz-confirm-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Booking…';

    fetch('/video-call/book/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify(state)
    })
      .then(function (res) { return res.ok ? res.json() : Promise.reject(); })
      .then(function () {
        if (typeof gtag === 'function') gtag('event', 'video_call_booked');
        document.getElementById('wiz-confirm-panel').innerHTML =
          '<h3>Call requested!</h3><p>We’ll confirm your slot by phone. You can see it under “Your calls” below.</p>';
        loadMyCalls();
      })
      .catch(function () {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Confirm booking';
        alert('Something went wrong booking that. Please try again or WhatsApp us at 098410 66880.');
      });
  }

  function loadMyCalls() {
    fetch('/video-call/my-calls/')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        renderCallList('upcoming', data.upcoming);
        renderCallList('history', data.history);
      })
      .catch(function () {
        // fail silently — section just shows the empty state
      });
  }

  var ICON_CAL = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>';
  var ICON_CLOCK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>';
  var ICON_PIN = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="11" r="2.5"/></svg>';

  function renderCallList(kind, calls) {
    var container = document.getElementById('my-calls-' + kind);
    if (!calls || calls.length === 0) {
      container.innerHTML = '<p class="my-calls-empty">No ' + kind + ' calls yet.</p>';
      return;
    }
    container.innerHTML = calls.map(function (c) {
      return '<div class="call-item">' +
        '<div class="call-info">' +
          '<h4>' + c.name + '</h4>' +
          '<div class="call-meta">' +
            '<span>' + ICON_CAL + ' ' + c.date + '</span>' +
            '<span>' + ICON_CLOCK + ' ' + c.time + '</span>' +
            '<span>' + ICON_PIN + ' ' + c.location + '</span>' +
          '</div>' +
        '</div>' +
        '<span class="call-badge">' + kind + '</span>' +
      '</div>';
    }).join('');
  }

  function initTabs() {
    var tabs = document.querySelectorAll('.my-calls-tab');
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) { t.classList.remove('is-active'); });
        tab.classList.add('is-active');
        var target = tab.getAttribute('data-target');
        document.querySelectorAll('.my-calls-panel').forEach(function (p) {
          p.style.display = (p.id === target) ? 'block' : 'none';
        });
      });
    });
  }

  var PHONE_PATTERN = /^\d{10}$/;
  var LOCATION_PATTERN = /^[A-Za-z\s]+-\s*[A-Za-z\s]+$/;

  function setMinDate() {
    var dateInput = document.getElementById('wiz-date');
    var today = new Date();
    // Minimum selectable date is tomorrow — no past or same-day dates.
    today.setDate(today.getDate() + 1);
    var yyyy = today.getFullYear();
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var dd = String(today.getDate()).padStart(2, '0');
    dateInput.min = yyyy + '-' + mm + '-' + dd;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var wizard = document.getElementById('video-call-wizard');
    if (!wizard) return;

    renderSlots();
    initTabs();
    loadMyCalls();
    setMinDate();

    // Phone field: digits only, capped at 10 characters as the user types.
    var phoneInput = document.getElementById('wiz-phone');
    phoneInput.addEventListener('input', function () {
      phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 10);
    });

    document.getElementById('wiz-step1-next').addEventListener('click', function () {
      state.full_name = document.getElementById('wiz-full-name').value.trim();
      state.location = document.getElementById('wiz-location').value.trim();
      state.phone = phoneInput.value.trim();
      state.agreed = document.getElementById('wiz-agree').checked;

      if (!state.full_name) {
        alert('Please enter your full name.');
        return;
      }
      if (!PHONE_PATTERN.test(state.phone)) {
        alert('Phone number must be exactly 10 digits.');
        return;
      }
      if (!LOCATION_PATTERN.test(state.location)) {
        alert('Please enter location as "City - State", e.g. Chennai - Tamil Nadu.');
        return;
      }
      if (!state.agreed) {
        alert('Please confirm you agree to the MOQ/MOP policy.');
        return;
      }
      goToStep(2);
    });

    document.getElementById('wiz-step2-back').addEventListener('click', function () { goToStep(1); });
    document.getElementById('wiz-step2-next').addEventListener('click', function () {
      state.date = document.getElementById('wiz-date').value;
      var minDate = document.getElementById('wiz-date').min;
      if (!state.date || !state.time) {
        alert('Please pick a date and a time slot.');
        return;
      }
      if (state.date < minDate) {
        alert('Please choose a future date.');
        return;
      }
      goToStep(3);
    });

    document.getElementById('wiz-step3-back').addEventListener('click', function () { goToStep(2); });
    document.getElementById('wiz-confirm-btn').addEventListener('click', submitBooking);
  });
})();
