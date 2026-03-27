// Cruise Process Wiki — Shared JS
(function() {
  // ── Sidebar toggle ──
  const sidebar = document.getElementById('sidebar');
  const main    = document.querySelector('.main');
  const btn     = document.getElementById('sidebarToggle');

  function setSidebar(collapsed) {
    if (collapsed) {
      sidebar.classList.add('collapsed');
      main && main.classList.add('expanded');
      btn && btn.classList.add('collapsed');
      btn && (btn.textContent = '▶');
      localStorage.setItem('sidebarCollapsed', '1');
    } else {
      sidebar.classList.remove('collapsed');
      main && main.classList.remove('expanded');
      btn && btn.classList.remove('collapsed');
      btn && (btn.textContent = '◀');
      localStorage.setItem('sidebarCollapsed', '0');
    }
  }

  if (btn) {
    btn.addEventListener('click', () => setSidebar(!sidebar.classList.contains('collapsed')));
  }
  if (localStorage.getItem('sidebarCollapsed') === '1') setSidebar(true);

  // ── Sidebar accordion (L1 sections) ──
  document.querySelectorAll('.sidebar-l1').forEach(el => {
    el.addEventListener('click', () => {
      const l2 = el.nextElementSibling;
      if (l2 && l2.classList.contains('sidebar-l2')) {
        l2.classList.toggle('open');
      }
    });
  });

  // ── Auto-open active section ──
  const activeLink = document.querySelector('.sidebar-l2-link.active');
  if (activeLink) {
    const l2 = activeLink.closest('.sidebar-l2');
    if (l2) l2.classList.add('open');
  }

  // ── Lightbox ──
  const diagWrap = document.querySelector('.diagram-wrap');
  const lb       = document.getElementById('lightbox');
  const lbImg    = document.getElementById('lightboxImg');
  const lbClose  = document.getElementById('lbClose');

  if (diagWrap && lb && lbImg) {
    diagWrap.addEventListener('click', () => {
      lbImg.src = diagWrap.querySelector('img').src;
      lb.classList.add('active');
    });
    lb.addEventListener('click', (e) => {
      if (e.target === lb || e.target === lbClose) lb.classList.remove('active');
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') lb.classList.remove('active');
    });
  }

  // ── Search ──
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.toLowerCase();
      document.querySelectorAll('.domain-card').forEach(card => {
        card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
      });
    });
  }
})();
