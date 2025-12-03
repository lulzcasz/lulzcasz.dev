document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll('.dropdown-menu .submenu-toggle').forEach(function(element){
        element.addEventListener('click', function (e) {
            
            e.stopPropagation();
            e.preventDefault();

            let nextEl = this.nextElementSibling;
            
            if(nextEl && nextEl.classList.contains('dropdown-menu')){
                let parent = this.closest('.dropdown-menu');
                if(parent){
                    parent.querySelectorAll('.show').forEach(function(submenu){
                        if(submenu !== nextEl){
                            submenu.classList.remove('show');
                        }
                    });
                }

                nextEl.classList.toggle('show');
            }
        });
    });

    const mainExploreNav = document.getElementById('main-explore-nav');

    if (mainExploreNav) {
        mainExploreNav.addEventListener('hidden.bs.dropdown', function () {
            const openSubmenus = mainExploreNav.querySelectorAll('.dropdown-menu.show');
            openSubmenus.forEach(function (submenu) {
                submenu.classList.remove('show');
            });
        });
    }
});
