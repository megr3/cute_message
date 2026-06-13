document.getElementById('msgForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevents the page from reloading or redirecting

    const submitBtn = document.getElementById('submitBtn');
    const statusDiv = document.getElementById('statusMessage');

    // 1. Extract values from the form inputs
    const rawencodedName = encodeURIComponent(userName);
    const rawencodedJoke = encodeURIComponent(userJoke);
    const rawencodedReceiver = encodeURIComponent(userReceiverName);
    const rawencodedNote = encodeURIComponent(note);

    // 2. Safely URL encode data exactly as your deployed application expects
    const encodedName = encodeURIComponent(rawencodedName);
    const encodedJoke = encodeURIComponent(rawencodedJoke);
    const encodedReceiver = encodeURIComponent(rawencodedReceiver);
    const encodedNote = encodeURIComponent(rawencodedNote);

    // Update UI button text to show active submission progress
    submitBtn.innerText = "Sending... 🚀";
    submitBtn.disabled = true;

    /* 
       Replace 'YOUR_FORMSPREE_ENDPOINT_ID' with a free endpoint id from formspree.io
       Or swap out this URL with any web database/webhook API setup you prefer.
    */
    const endpoint = 'https://formspree.io';

    // 3. Dispatch data asynchronously behind the scenes
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: encodedName,
            joke: encodedJoke,
            receiver: encodedReceiver,
            note: encodedNote
        })
    })
    .then(response => {
        if (response.ok) {
            // Give her a gorgeous inline validation response instead of transferring screens
            statusDiv.innerText = "Message sent successfully! ❤️";
            statusDiv.style.color = "#2a9d8f";
            statusDiv.style.display = "block";
            
            // Wipe input values clean so she knows submission completed
            document.getElementById('msgForm').reset();
        } else {
            throw new Error('Network payload failure.');
        }
    })
    .catch(error => {
        statusDiv.innerText = "Oops! Something went wrong. Please try again.";
        statusDiv.style.color = "#e63946";
        statusDiv.style.display = "block";
    })
    .finally(() => {
        // Return button state to clickable default layout
        submitBtn.innerText = "Send Message ✨";
        submitBtn.disabled = false;
    });
});
