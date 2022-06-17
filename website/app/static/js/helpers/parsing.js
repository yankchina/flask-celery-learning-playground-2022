
function htmlToElement(html) {
    /* when given html as a string, this converts it into an html dom node ready to be appended to a parent */
    var template = document.createElement('template');
    template.innerHTML = html;
    return template.content.firstChild;
}