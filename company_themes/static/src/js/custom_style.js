function applyCompanyClass() {
    let navbarElement = document.querySelector(".o_main_navbar .oe_topbar_name");

    if (navbarElement) {
        let companyName = navbarElement.textContent.trim();
        if (companyName) {
            let sanitizedCompanyName = companyName.replace(/\s+/g, '-').toLowerCase();
            document.body.classList.forEach(cls => {
                if (cls.startsWith("company-")) {
                    document.body.classList.remove(cls);
                }
            });
            document.body.classList.add("company-" + sanitizedCompanyName);
        }
    } else {
        setTimeout(applyCompanyClass, 500);
    }
}

document.addEventListener("DOMContentLoaded", applyCompanyClass);
