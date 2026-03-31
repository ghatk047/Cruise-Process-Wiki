/* Cruise Process Wiki JS — v2 clean rewrite */

const DOMAIN_ICONS = {
  'guest': '🚢', 'embarkation': '🚢', 'debarkation': '🚢', 'concierge': '🚢',
  'stateroom': '🛏️', 'housekeeping': '🛏️', 'laundry': '🧺',
  'food': '🍽️', 'beverage': '🍽️', 'dining': '🍽️', 'culinary': '👨‍🍳',
  'entertainment': '🎭', 'activities': '🎠', 'showroom': '🎭',
  'shore': '⚓', 'excursion': '⚓', 'destination': '🏝️',
  'marine': '⚙️', 'technical': '⚙️', 'engineering': '⚙️', 'navigation': '🧭',
  'environmental': '🌿', 'sustainability': '🌿', 'waste': '♻️',
  'crew': '👥', 'management': '👥',
  'revenue': '💰', 'commercial': '💰', 'loyalty': '🏅',
  'finance': '💼', 'procurement': '📦',
  'technology': '💻', 'cybersecurity': '🔐',
  'health': '🏥', 'safety': '🛡️', 'medical': '⚕️',
  'ea': '🗺️',
};

function getDomainIcon(name) {
  var lower = (name || '').toLowerCase();
  var keys = Object.keys(DOMAIN_ICONS);
  for (var i = 0; i < keys.length; i++) {
    if (lower.indexOf(keys[i]) !== -1) return DOMAIN_ICONS[keys[i]];
  }
  return '📋';
}

document.addEventListener('DOMContentLoaded', function() {

  /* ── 1. INJECT ICONS ── */
  document.querySelectorAll('.sidebar-domain').forEach(function(el) {
    var labelEl = el.querySelector('.sidebar-domain-label') || el;
    var text = labelEl.textContent.trim();
    el.setAttribute('data-label', text);
    if (!el.querySelector('.domain-icon')) {
      var ic = document.createElement('span');
      ic.className = 'domain-icon';
      ic.textContent = getDomainIcon(text);
      el.insertBefore(ic, el.firstChild);
    }
  });

  /* ── 2. SIDEBAR ELEMENTS ── */
  var sidebar   = document.getElementById('sidebar');
  var mainEl    = document.querySelector('.main');
  var toggleBtn = document.getElementById('sidebarToggle');
  var RAIL_W    = 52;
  var currentW  = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w')) || 260;

  function isMobile() { return window.innerWidth <= 900; }

  /* Inject resizer */
  var resizer = document.getElementById('sidebar-resizer');
  if (!resizer && sidebar) {
    resizer = document.createElement('div');
    resizer.id = 'sidebar-resizer';
    document.body.appendChild(resizer);
  }

  /* Inject overlay */
  var overlay = document.getElementById('sidebar-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'sidebar-overlay';
    document.body.appendChild(overlay);
  }

  /* ── 3. COLLAPSE / EXPAND ── */
  function setSidebarRail() {
    if (!sidebar) return;
    sidebar.classList.add('rail');
    sidebar.classList.remove('mobile-open');
    if (toggleBtn) { toggleBtn.innerHTML = '&#9654;'; toggleBtn.title = 'Expand sidebar'; }
    if (resizer) resizer.style.left = RAIL_W + 'px';
    try { localStorage.setItem('sidebarState', 'rail'); } catch(e) {}
  }

  function setSidebarExpanded() {
    if (!sidebar) return;
    sidebar.classList.remove('rail');
    sidebar.style.width = currentW + 'px';
    if (mainEl) mainEl.style.marginLeft = currentW + 'px';
    if (resizer) resizer.style.left = currentW + 'px';
    if (toggleBtn) {
      toggleBtn.style.left = (currentW - 14) + 'px';
      toggleBtn.innerHTML = '&#9664;';
      toggleBtn.title = 'Collapse sidebar';
    }
    try { localStorage.setItem('sidebarState', 'expanded'); } catch(e) {}
  }

  /* ── 4. SIDEBAR ACCORDION ── */
  document.querySelectorAll('.sidebar-domain').forEach(function(el) {
    el.addEventListener('click', function() {
      if (sidebar && sidebar.classList.contains('rail')) {
        setSidebarExpanded();
        setTimeout(function() {
          el.classList.add('open');
          var l2 = el.nextElementSibling;
          if (l2) l2.classList.add('open');
        }, 230);
        return;
      }
      el.classList.toggle('open');
      var l2 = el.nextElementSibling;
      if (l2) l2.classList.toggle('open');
    });
  });

  /* Auto-open active section */
  var active = document.querySelector('.sidebar-l3-link.active');
  if (active) {
    var l2 = active.closest('.sidebar-l2');
    if (l2) {
      l2.classList.add('open');
      var d = l2.previousElementSibling;
      if (d) d.classList.add('open');
    }
  }

  /* ── 5. TOGGLE BUTTON ── */
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function() {
      if (isMobile()) {
        if (sidebar.classList.contains('mobile-open')) {
          sidebar.classList.remove('mobile-open');
          overlay.classList.remove('active');
          toggleBtn.innerHTML = '&#9654;';
        } else {
          sidebar.classList.add('mobile-open');
          overlay.classList.add('active');
          toggleBtn.innerHTML = '&#9664;';
        }
      } else {
        if (sidebar && sidebar.classList.contains('rail')) {
          setSidebarExpanded();
        } else {
          setSidebarRail();
        }
      }
    });
  }

  overlay.addEventListener('click', function() {
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
    if (toggleBtn) toggleBtn.innerHTML = '&#9654;';
  });

  /* ── 6. HOVER EXPAND FROM RAIL ── */
  if (sidebar) {
    sidebar.addEventListener('mouseenter', function() {
      if (!isMobile() && sidebar.classList.contains('rail')) setSidebarExpanded();
    });
  }

  /* ── 7. DRAG RESIZE ── */
  if (resizer) {
    var dragging = false, startX, startW;
    resizer.addEventListener('mousedown', function(e) {
      if (isMobile()) return;
      dragging = true; startX = e.clientX; startW = sidebar ? sidebar.offsetWidth : currentW;
      resizer.classList.add('dragging');
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
      e.preventDefault();
    });
    document.addEventListener('mousemove', function(e) {
      if (!dragging || !sidebar) return;
      var newW = Math.max(180, Math.min(480, startW + e.clientX - startX));
      if (newW < 120) { setSidebarRail(); dragging = false; return; }
      currentW = newW;
      sidebar.style.width = newW + 'px';
      if (mainEl) mainEl.style.marginLeft = newW + 'px';
      resizer.style.left = newW + 'px';
      if (toggleBtn) toggleBtn.style.left = (newW - 14) + 'px';
      document.documentElement.style.setProperty('--sidebar-w', newW + 'px');
      sidebar.classList.remove('rail');
    });
    document.addEventListener('mouseup', function() {
      if (!dragging) return;
      dragging = false;
      resizer.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      try { localStorage.setItem('sidebarW', currentW); } catch(e) {}
    });
  }

  /* ── 8. RESTORE STATE ── */
  try {
    var savedState = localStorage.getItem('sidebarState');
    var savedW     = localStorage.getItem('sidebarW');
    if (!isMobile()) {
      if (savedW) {
        currentW = parseInt(savedW);
        document.documentElement.style.setProperty('--sidebar-w', currentW + 'px');
      }
      if (savedState === 'rail') {
        setSidebarRail();
      } else {
        setSidebarExpanded();
      }
    }
  } catch(e) {}

  window.addEventListener('resize', function() {
    if (!isMobile()) {
      overlay.classList.remove('active');
      if (sidebar) sidebar.classList.remove('mobile-open');
    }
  });

  /* ── 9. SMOOTH SCROLL ── */
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var t = document.querySelector(a.getAttribute('href'));
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

  /* ── 10. BPMN LIGHTBOX WITH ZOOM + PAN ── */
  function buildLightbox() {
    /* If already built (has toolbar), return it */
    var existing = document.getElementById('bpmn-lightbox');
    if (existing && document.getElementById('lb-toolbar')) return existing;

    /* Build the lightbox div */
    var ov = document.createElement('div');
    ov.id = 'bpmn-lightbox';
    ov.innerHTML =
      '<div id="lb-toolbar">' +
        '<span id="lb-title">Process Flow Diagram</span>' +
        '<div id="lb-controls">' +
          '<button id="lb-zoom-in" title="Zoom in">+</button>' +
          '<button id="lb-zoom-out" title="Zoom out">&#8722;</button>' +
          '<button id="lb-reset" title="Reset view">Reset</button>' +
          '<button id="lb-close" title="Close (Esc)">&#10005;</button>' +
        '</div>' +
      '</div>' +
      '<div id="lb-canvas"><img id="lb-img" src="" alt="diagram" draggable="false"></div>' +
      '<div id="lb-hint">Drag to pan &nbsp;|&nbsp; Scroll to zoom &nbsp;|&nbsp; Esc to close</div>';

    /* Replace empty placeholder or append to body */
    var placeholder = document.getElementById('bpmn-lightbox');
    if (placeholder && !document.getElementById('lb-toolbar')) {
      placeholder.parentNode.replaceChild(ov, placeholder);
    } else if (!placeholder) {
      document.body.appendChild(ov);
    }

    var canvas = document.getElementById('lb-canvas');
    var img    = document.getElementById('lb-img');
    var scale = 1, ox = 0, oy = 0, lbDragging = false, lx = 0, ly = 0;

    function applyT() { img.style.transform = 'translate(' + ox + 'px,' + oy + 'px) scale(' + scale + ')'; }
    function resetView() { scale = 1; ox = 0; oy = 0; applyT(); }
    function closeLB() { ov.classList.remove('lb-open'); resetView(); }

    document.getElementById('lb-zoom-in').onclick  = function() { scale = Math.min(scale * 1.3, 8); applyT(); };
    document.getElementById('lb-zoom-out').onclick = function() { scale = Math.max(scale / 1.3, 0.15); applyT(); };
    document.getElementById('lb-reset').onclick    = resetView;
    document.getElementById('lb-close').onclick    = closeLB;

    canvas.addEventListener('wheel', function(e) {
      e.preventDefault();
      scale = e.deltaY < 0 ? Math.min(scale * 1.1, 8) : Math.max(scale / 1.1, 0.15);
      applyT();
    }, { passive: false });

    canvas.addEventListener('mousedown', function(e) {
      lbDragging = true; lx = e.clientX; ly = e.clientY;
      img.style.cursor = 'grabbing';
    });
    document.addEventListener('mousemove', function(e) {
      if (!lbDragging) return;
      ox += e.clientX - lx; oy += e.clientY - ly;
      lx = e.clientX; ly = e.clientY; applyT();
    });
    document.addEventListener('mouseup', function() {
      lbDragging = false; img.style.cursor = 'grab';
    });

    /* Touch pan + pinch */
    var lastDist = 0;
    canvas.addEventListener('touchstart', function(e) {
      e.preventDefault();
      if (e.touches.length === 1) { lbDragging = true; lx = e.touches[0].clientX; ly = e.touches[0].clientY; }
      else if (e.touches.length === 2) { lastDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY); }
    }, { passive: false });
    canvas.addEventListener('touchmove', function(e) {
      e.preventDefault();
      if (e.touches.length === 1 && lbDragging) {
        ox += e.touches[0].clientX - lx; oy += e.touches[0].clientY - ly;
        lx = e.touches[0].clientX; ly = e.touches[0].clientY; applyT();
      } else if (e.touches.length === 2) {
        var d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
        scale = Math.min(Math.max(scale * (d / lastDist), 0.15), 8);
        lastDist = d; applyT();
      }
    }, { passive: false });
    canvas.addEventListener('touchend', function() { lbDragging = false; });

    document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeLB(); });
    ov.addEventListener('click', function(e) { if (e.target === ov || e.target === canvas) closeLB(); });

    return ov;
  }

  /* Attach lightbox to all diagram images */
  document.querySelectorAll('.diagram-wrap img').forEach(function(img) {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', function() {
      var lb = buildLightbox();
      document.getElementById('lb-img').src = img.src;
      lb.classList.add('lb-open');
    });
  });

  /* ── 11. SEARCH ── */
  var searchBox = document.getElementById('searchBox') || document.querySelector('input.search-box');
  if (searchBox) {
    var resultsEl = document.getElementById('searchResults');
    if (!resultsEl) {
      resultsEl = document.createElement('div');
      resultsEl.id = 'searchResults';
      resultsEl.className = 'search-results';
      resultsEl.style.display = 'none';
      var wrap = searchBox.closest('.topbar-search');
      if (wrap) wrap.appendChild(resultsEl);
      else document.body.appendChild(resultsEl);
    }

    var links = Array.prototype.slice.call(document.querySelectorAll('.sidebar-l3-link')).map(function(a) {
      return { text: a.textContent.replace(/\s+/g, ' ').trim(), href: a.href };
    });

    searchBox.addEventListener('input', function() {
      var q = searchBox.value.trim().toLowerCase();
      if (!q) { resultsEl.style.display = 'none'; return; }
      var hits = links.filter(function(l) { return l.text.toLowerCase().indexOf(q) !== -1; }).slice(0, 8);
      if (!hits.length) { resultsEl.style.display = 'none'; return; }
      resultsEl.innerHTML = hits.map(function(h) {
        return '<a class="sr-item" href="' + h.href + '">' + h.text + '</a>';
      }).join('');
      resultsEl.style.display = 'block';
    });

    document.addEventListener('click', function(e) {
      if (!searchBox.contains(e.target) && !resultsEl.contains(e.target)) {
        resultsEl.style.display = 'none';
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === '/' && document.activeElement !== searchBox) {
        e.preventDefault(); searchBox.focus();
      }
      if (e.key === 'Escape') {
        searchBox.value = ''; resultsEl.style.display = 'none'; searchBox.blur();
      }
    });
  }

  /* ── 12. STATUS DOTS ── */
  document.querySelectorAll('.sidebar-l3-link').forEach(function(link) {
    var dot = link.querySelector('.status-dot');
    if (dot) {
      if (dot.classList.contains('status-done')) dot.title = 'Complete';
      else if (dot.classList.contains('status-wip')) dot.title = 'In Progress';
      else dot.title = 'Queued';
    }
  });

  /* ── 13. INJECT EA SECTION into sidebars missing it (process pages pre-fix) ── */
  (function() {
    var sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    // Check if EA section already present
    if (sidebar.innerHTML.indexOf('EA Diagrams') !== -1) return;

    // Determine path prefix from current URL depth
    var path = window.location.pathname;
    // Count segments after the repo root
    var parts = path.replace(/\/+$/, '').split('/').filter(Boolean);
    // Remove repo name (Cruise-Process-Wiki)
    var idx = parts.indexOf('Cruise-Process-Wiki');
    var depth = idx >= 0 ? parts.length - idx - 1 : parts.length;
    var prefix = '';
    for (var i = 0; i < depth; i++) prefix += '../';

    var eaTitles = [
      'Cruise Integrated System Landscape',
      'Guest Journey Data Flow',
      'Shipboard Operations Architecture',
      'Onboard Revenue Architecture',
      'Marine & Environmental Architecture',
      'Crew Management & HR Integration',
      'Connectivity & Digital Infrastructure',
      'Finance & Procurement Architecture',
      'Safety, Security & Medical Architecture',
      'Loyalty & CRM Architecture'
    ];

    var links = '<a class="sidebar-l3-link" href="' + prefix + 'ea-diagrams/">All EA Diagrams</a>';
    for (var n = 1; n <= 10; n++) {
      var eid = 'EA-' + (n < 10 ? '0' : '') + n;
      links += '<a class="sidebar-l3-link" href="' + prefix + 'ea-diagrams/' + eid.toLowerCase() + '/">' +
               '<span class="pid">' + eid + '</span>' + eaTitles[n-1] + '</a>';
    }

    var divider = document.createElement('div');
    divider.style.cssText = 'height:1px;background:#dde1e8;margin:8px 14px';

    var section = document.createElement('div');
    section.className = 'sidebar-section';
    section.innerHTML =
      '<div class="sidebar-domain" data-label="EA Diagrams">' +
        '<span class="sidebar-domain-label">🗺️ EA Diagrams</span>' +
        '<span class="chevron">▶</span>' +
      '</div>' +
      '<div class="sidebar-l2">' + links + '</div>';

    sidebar.appendChild(divider);
    sidebar.appendChild(section);

    // Wire accordion for new section
    var newDomain = section.querySelector('.sidebar-domain');
    if (newDomain) {
      newDomain.addEventListener('click', function() {
        newDomain.classList.toggle('open');
        var l2 = newDomain.nextElementSibling;
        if (l2) l2.classList.toggle('open');
      });
    }
  })();


});
