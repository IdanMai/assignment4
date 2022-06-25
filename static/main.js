const activePage = window.location.pathname;

document.querySelectorAll('header a')?.forEach(link => {
    if (link.href.includes(activePage))
        link.classList.add('active-nav');
})

// animate a twist for the house image
document.querySelector('.home-page__container img')?.addEventListener('click', (e) => {
    console.log(e.target)
    if (e.target.className === 'spin')
        e.target.className = ''
    else
        e.target.className = 'spin'
})

document.querySelector('#outer-source__form')?.addEventListener('submit',(e)=> {
    e.preventDefault()
    const id = e.target.id.value
    fetch('https://reqres.in/api/users/' + id)
        .then(results => results.json())
        .then(json => {
            const image = document.querySelector('#outer-source__image1')
            image.classList.remove('invisible')
            image.src = json.data.avatar
        })
        .catch((e) => {
        console.log(e)
        })
})
