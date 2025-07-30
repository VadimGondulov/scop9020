$(document).ready(function() {
    let counter = 1;

    $('#add-btn').click(function() {
        const newInput = `<input type="text" name="name${counter}" placeholder="Enter name">`;
        $('#input-container').append(newInput);
        counter++;
    });
    
    $('#name-form').submit(function(e) {
//        e.preventDefault();
        alert('Form is sended succesfully!');
    });
});
