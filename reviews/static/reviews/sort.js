const sort = document.getElementById('sort-by');
if (sort) {
    sort.addEventListener('change', (elem) => {
        const select = elem.target;
        select.form.submit();
    }) 
}