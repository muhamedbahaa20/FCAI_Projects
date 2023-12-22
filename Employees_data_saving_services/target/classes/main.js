function searchByGpa() {
    const gpa = document.getElementById("gpa").value;
    fetch(`/students/?gpa=${gpa}`)
        .then(response => response.json())
        .then(students => {
            displayStudents(students);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function searchByFirstName() {
    const firstName = document.getElementById("firstName").value;
    fetch(`/students/?firstName=${firstName}`)
        .then(response => response.json())
        .then(students => {
            displayStudents(students);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function saveStudent() {
    const id = document.getElementById("id").value;
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const gender = document.getElementById("gender").value;
    const gpa = document.getElementById("gpa").value;
    const level = document.getElementById("level").value;
    const address = document.getElementById("address").value;

    const student = {
        id: id,
        firstName: firstName,
        lastName: lastName,
        gender: gender,
        gpa: gpa,
        level: level,
        address: address
    }
    const url = "http://localhost:8080/addStudent";

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(student),
    })
        .then(response => response.text())
        .then(data => {
            // Handle the response from the server
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });


}

function deleteStudent() {
    const id = document.getElementById("deleteId").value;
    fetch(`/students/${id}`, { method: 'DELETE' })
        .then(response => response.text())
        .then(message => {
            console.log(message);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function displayStudents(students) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    if (students.length === 0) {
        resultDiv.innerHTML = "No students found.";
        return;
    }

    const table = document.createElement("table");
    const headerRow = document.createElement("tr");
    const idHeader = document.createElement("th");
    idHeader.textContent = "ID";
    const firstNameHeader = document.createElement("th");
    firstNameHeader.textContent = "First Name";
    const lastNameHeader = document.createElement("th");
    lastNameHeader.textContent = "Last Name";
    const genderHeader = document.createElement("th");
}