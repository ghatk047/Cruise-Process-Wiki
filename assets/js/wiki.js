/* Cruise Process Wiki JS — Light theme, zoom+pan lightbox, rail sidebar, search */

const DOMAIN_ICONS = {
  'guest':         '🚢', 'embarkation': '🚢', 'debarkation': '🚢', 'concierge': '🚢',
  'stateroom':     '🛏️', 'housekeeping': '🛏️', 'laundry': '🧺',
  'food':          '🍽️', 'beverage': '🍽️', 'dining': '🍽️', 'culinary': '👨‍🍳',
  'entertainment': '🎭', 'activities': '🎠', 'showroom': '🎭',
  'shore':         '⚓', 'excursion': '⚓', 'destination': '🏝️',
  'marine':        '⚙️', 'technical': '⚙️', 'engineering': '⚙️', 'navigation': '🧭',
  'environmental': '🌿', 'sustainability': '🌿', 'waste': '♻️',
  'crew':          '👥', 'management': '👥', 'hr': '👥',
  'revenue':       '💰', 'commercial': '💰', 'loyalty': '🏅',
  'finance':       '💼', 'procurement': '📦',
  'technology':    '💻', 'cybersecurity': '🔐', 'it': '💻',
  'health':        '🏥', 'safety': '🛡️', 'medical': '⚕️',
};

function getDomainIcon(name) {
  const lower = (name || '').toLowerCase();
  for (const [key, icon] of Object.entries(DOMAIN_ICONS)) {
    if (lower.includes(key)) return icon;
  }
  return '📋';
}

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. INJECT ICONS into sidebar domain headers ── */
  document.querySelectorAll('.sidebar-domain').forEach(el => {
    const labelEl = el.querySelector('.sidebar-domain-label') || el;
    const text = labelEl.textContent.trim();
    el.setAttribute('data-label', text);
    if (!el.querySelector('.domain-icon')) {
      const ic = document.createElement('span');
      ic.className = 'domain-icon';
      ic.textContent = getDomainIcon(text);
      el.insertBefore(ic, el.firstChild);
    }
  });

  /* ── 2. SIDEBAR ELEMENTS ── */
  const sidebar   = document.getElementById('sidebar');
  const mainEl    = document.querySelector('.main');
  const toggleBtn = document.getElementById('sidebarToggle');
  const isMobile  = () => window.innerWidth <= 900;
  const RAIL_W    = 52;
  let currentW    = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w')) || 260;

  /* Inject drag resizer */
  let resizer = document.getElementById('sidebar-resizer');
  if (!resizer && sidebar) {
    resizer = document.createElement('div');
    resizer.id = 'sidebar-resizer';
    document.body.appendChild(resizer);
  }
  /* Inject overlay */
  let overlay = document.getElementById('sidebar-overlay');
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
    localStorage.setItem('sidebarState', 'rail');
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
    localStorage.setItem('sidebarState', 'expanded');
  }

  /* ── 4. SIDEBAR ACCORDION ── */
  document.querySelectorAll('.sidebar-domain').forEach(el => {
    el.addEventListener('click', () => {
      if (sidebar && sidebar.classList.contains('rail')) {
        setSidebarExpanded();
        setTimeout(() => {
          el.classList.add('open');
          const l2 = el.nextElementSibling;
          if (l2) l2.classList.add('open');
        }, 230);
        return;
      }
      el.classList.toggle('open');
      const l2 = el.nextElementSibling;
      if (l2) l2.classList.toggle('open');
    });
  });

  /* Auto-open active section */
  const active = document.querySelector('.sidebar-l3-link.active');
  if (active) {
    const l2 = active.closest('.sidebar-l2');
    if (l2) {
      l2.classList.add('open');
      const d = l2.previousElementSibling;
      if (d) d.classList.add('open');
    }
  }

  /* ── 5. TOGGLE BUTTON ── */
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
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
        sidebar && sidebar.classList.contains('rail') ? setSidebarExpanded() : setSidebarRail();
      }
    });
  }

  overlay.addEventListener('click', () => {
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
    if (toggleBtn) toggleBtn.innerHTML = '&#9654;';
  });

  /* ── 6. HOVER EXPAND FROM RAIL ── */
  if (sidebar) {
    sidebar.addEventListener('mouseenter', () => {
      if (!isMobile() && sidebar.classList.contains('rail')) setSidebarExpanded();
    });
  }

  /* ── 7. DRAG RESIZE ── */
  if (resizer) {
    let dragging = false, startX, startW;
    resizer.addEventListener('mousedown', e => {
      if (isMobile()) return;
      dragging = true; startX = e.clientX; startW = sidebar ? sidebar.offsetWidth : currentW;
      resizer.classList.add('dragging');
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
      e.preventDefault();
    });
    document.addEventListener('mousemove', e => {
      if (!dragging || !sidebar) return;
      const newW = Math.max(180, Math.min(480, startW + e.clientX - startX));
      if (newW < 120) { setSidebarRail(); dragging = false; return; }
      currentW = newW;
      sidebar.style.width = newW + 'px';
      if (mainEl) mainEl.style.marginLeft = newW + 'px';
      resizer.style.left = newW + 'px';
      if (toggleBtn) toggleBtn.style.left = (newW - 14) + 'px';
      document.documentElement.style.setProperty('--sidebar-w', newW + 'px');
      sidebar.classList.remove('rail');
    });
    document.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      resizer.classList.remove('dragging');
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      localStorage.setItem('sidebarW', currentW);
    });
  }

  /* ── 8. RESTORE STATE ── */
  const savedState = localStorage.getItem('sidebarState');
  const savedW     = localStorage.getItem('sidebarW');
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

  window.addEventListener('resize', () => {
    if (!isMobile()) {
      overlay.classList.remove('active');
      if (sidebar) sidebar.classList.remove('mobile-open');
    }
  });

  /* ── 9. SMOOTH SCROLL ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

  /* ── 10. BPMN LIGHTBOX WITH ZOOM + PAN ── */
  function buildLightbox() {
    const existing = document.getElementById('bpmn-lightbox');
    if (existing && document.getElementById('lb-toolbar')) return existing;
    const ov = document.createElement('div');
    ov.id = 'bpmn-lightbox';
    ov.innerHTML = `
      <div id="lb-toolbar">
        <span id="lb-title">Process Flow Diagram (BPMN)</span>
        <div id="lb-controls">
          <button id="lb-zoom-in" title="Zoom in">+</button>
          <button id="lb-zoom-out" title="Zoom out">&#8722;</button>
          <button id="lb-reset" title="Reset view">Reset</button>
          <button id="lb-close" title="Close (Esc)">&#10005;</button>
        </div>
      </div>
      <div id="lb-canvas"><img id="lb-img" src="" alt="BPMN diagram" draggable="false"></div>
      <div id="lb-hint">Drag to pan &nbsp;|&nbsp; Scroll to zoom &nbsp;|&nbsp; Esc to close</div>`;
    const placeholder = document.getElementById('bpmn-lightbox');
    if (placeholder) {
      placeholder.id = 'bpmn-lightbox-old'; // rename so ov.id='bpmn-lightbox' is unique
      placeholder.parentNode.replaceChild(ov, placeholder);
    } else {
      document.body.appendChild(ov);
    }

    const canvas = document.getElementById('lb-canvas');
    const img    = document.getElementById('lb-img');
    let scale = 1, ox = 0, oy = 0, draggingLB = false, lx = 0, ly = 0;

    const applyT    = () => { img.style.transform = `translate(${ox}px,${oy}px) scale(${scale})`; };
    const resetView = () => { scale = 1; ox = 0; oy = 0; applyT(); };
    const closeLB   = () => { ov.classList.remove('lb-open'); resetView(); };

    document.getElementById('lb-zoom-in').onclick  = () => { scale = Math.min(scale * 1.3, 8); applyT(); };
    document.getElementById('lb-zoom-out').onclick = () => { scale = Math.max(scale / 1.3, 0.15); applyT(); };
    document.getElementById('lb-reset').onclick    = resetView;
    document.getElementById('lb-close').onclick    = closeLB;

    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      scale = e.deltaY < 0 ? Math.min(scale * 1.1, 8) : Math.max(scale / 1.1, 0.15);
      applyT();
    }, { passive: false });

    canvas.addEventListener('mousedown', e => {
      draggingLB = true; lx = e.clientX; ly = e.clientY;
      img.style.cursor = 'grabbing';
    });
    document.addEventListener('mousemove', e => {
      if (!draggingLB) return;
      ox += e.clientX - lx; oy += e.clientY - ly;
      lx = e.clientX; ly = e.clientY; applyT();
    });
    document.addEventListener('mouseup', () => { draggingLB = false; img.style.cursor = 'grab'; });

    /* Touch: pan + pinch-zoom */
    let lastDist = 0;
    canvas.addEventListener('touchstart', e => {
      e.preventDefault();
      if (e.touches.length === 1) { draggingLB = true; lx = e.touches[0].clientX; ly = e.touches[0].clientY; }
      else if (e.touches.length === 2) {
        lastDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      }
    }, { passive: false });
    canvas.addEventListener('touchmove', e => {
      e.preventDefault();
      if (e.touches.length === 1 && draggingLB) {
        ox += e.touches[0].clientX - lx; oy += e.touches[0].clientY - ly;
        lx = e.touches[0].clientX; ly = e.touches[0].clientY; applyT();
      } else if (e.touches.length === 2) {
        const d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
        scale = Math.min(Math.max(scale * (d / lastDist), 0.15), 8);
        lastDist = d; applyT();
      }
    }, { passive: false });
    canvas.addEventListener('touchend', () => { draggingLB = false; });

    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLB(); });
    ov.addEventListener('click', e => { if (e.target === ov || e.target === canvas) closeLB(); });

    return ov;
  }

  /* Attach lightbox to all diagram images */
  document.querySelectorAll('.diagram-wrap img').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', () => {
      const lb = buildLightbox();
      document.getElementById('lb-img').src = img.src;
      lb.classList.add('lb-open');
    });
  });

  /* ── 11. SEARCH (topbar searchBox) ── */
  const searchBox = document.getElementById('searchBox');
  if (searchBox) {
      searchBox.closest('.topbar-search') ?
    }

    const links = [...document.querySelectorAll('.sidebar-l3-link')].map(a => ({
      text: a.textContent.replace(/\s+/g, ' ').trim(), href: a.href
    }));

    
  /* ── SEARCH — redirect to search.html on Enter ── */
  const searchBox = document.getElementById('searchBox');
  if (searchBox) {
    function getSearchUrl(q) {
      const logo = document.querySelector('a.topbar-logo, a[class*="logo"]');
      const base = logo ? logo.getAttribute('href') : '/';
      const root = base.endsWith('/') ? base : base + '/';
      return root + 'search.html?q=' + encodeURIComponent(q.trim());
    }
    searchBox.addEventListener('keydown', e => {
      if (e.key === 'Enter' && searchBox.value.trim()) {
        window.location.href = getSearchUrl(searchBox.value);
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key === '/' && document.activeElement !== searchBox) {
        e.preventDefault(); searchBox.focus(); searchBox.select();
      }
      if (e.key === 'Escape' && document.activeElement === searchBox) {
        searchBox.value = ''; searchBox.blur();
      }
    });
  }


});

});
