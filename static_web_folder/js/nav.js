const views = document.getElementsByClassName("View");
var animationLock = false;
var animationUnlockFunc = undefined;

const changeView = (element, id) => {
    if (!animationLock) {
        animationLock = true;
        const links = document.getElementsByClassName("Link");
        for (let e of links) {
            e.classList.remove("Active")
        }
        element.classList.add("Active");

        // Animation
        for (let v of views) {
            // Current view
            v.classList.remove("InstantAnimation");

            if (v.id == id) {
                v.classList.remove("AnimateOut");
                v.classList.add("AnimateIn");
                // View to be animated out
            } else {
                v.classList.add("AnimateOut");
                v.classList.remove("AnimateIn");
            }
        }
        animationUnlockFunc = setInterval(() => {
            animationLock = false; clearInterval(animationUnlockFunc)
        }, 300)
    }
}