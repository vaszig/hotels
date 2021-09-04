const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')

const sendSearchData = (city) => {
    fetch("api/search/?city=" + city)
        .then(response => response.json())
        .then(response_data => {
            if (response_data.data.length === 0){
                resultsBox.innerHTML = `No cities found`
            }else{
                resultsBox.innerHTML = ''
                response_data.data.forEach(element => {
                    resultsBox.innerHTML += `<p><b>City: ${ element.city }</b>`
                    resultsBox.innerHTML += `<ul></ul>`
                    element.hotels.forEach(hotel => {
                        resultsBox.innerHTML += `<li>${hotel}</li>`
                    })
                    resultsBox.innerHTML += `</p>`
            })}
        })
}

searchInput.addEventListener('keyup', e => {

    sendSearchData(e.target.value)

})
