
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('logo-sidebar');
    if (!sidebar) return;
    let isDesktop = window.innerWidth >= 768;
    let wasDesktop = isDesktop;
    function handleSidebarResponsive() {
      isDesktop = window.innerWidth >= 768;
      if (isDesktop) {
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        const backdrop = document.querySelector('[drawer-backdrop]');
        if (backdrop) {
          backdrop.style.opacity = '0';
          setTimeout(() => { backdrop.style.display = 'none'; }, 300);
        }
      } else if (wasDesktop && !isDesktop) {
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
      }
      wasDesktop = isDesktop;
    }
    handleSidebarResponsive();
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(handleSidebarResponsive, 100);
    });
    const backdropObserver = new MutationObserver(function() {
      if (!isDesktop) {
        const backdrop = document.querySelector('[drawer-backdrop]');
        if (backdrop && backdrop.style.display !== 'none') {
          backdrop.style.opacity = '1';
        }
      }
    });
    backdropObserver.observe(document.body, { childList: true, subtree: true });
  });

