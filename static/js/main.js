function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

items = document.getElementsByClassName('icons-container')

for (let item of items){
    const [like,count,dislike] = item.children;
    console.log(like.dataset)
    like.addEventListener('click', () => {
        // count.innerHTML = Number(count.innerHTML) + 1;
        // if (item)
        const formData = new FormData()
        formData.append('id', like.dataset.id)
        formData.append('type', like.dataset.type)
        formData.append('mark', '1')
        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                count.innerHTML = data.count;
                // counter.innerHTML = data.counter
            })

        // alert('Hello');
    })
    dislike.addEventListener('click', () => {
        // count.innerHTML = Number(count.innerHTML) + 1;
        // if (item)
        const formData = new FormData()
        formData.append('id', like.dataset.id)
        formData.append('type', like.dataset.type)
        formData.append('mark', '-1')
        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                count.innerHTML = data.count;
                // counter.innerHTML = data.counter
            })

        // alert('Hello');
    })
}
corrects = document.getElementsByClassName('correct')
for (let cor of corrects) {
    cor.addEventListener('click', ()=>{
        const formData = new FormData()
        formData.append('id', cor.dataset.id)
        const request = new Request('/correct/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
    })
}