const countrySelect = document.getElementById('country-select');
const loadDataBtn = document.getElementById('load-data');
const studentDataContainer = document.getElementById('student-data');
const studentFormContainer = document.getElementById('student-form');
const updatedDataContainer = document.getElementById('updated-data');

loadDataBtn.addEventListener('click', function() {
  const selectedCountry = countrySelect.value;

  if (!selectedCountry) {
    alert('Please select a country');
    return;
  }

  fetch('http://192.155.90.208/students.json')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      const filteredStudents = data.filter(student => student.country === selectedCountry);
      displayStudents(filteredStudents);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      studentDataContainer.innerHTML = '<p>Error fetching student data.</p>';
    });
});

function displayStudents(students) {
  if (!students.length) {
    studentDataContainer.innerHTML = '<p>No students found for selected country.</p>';
    return;
  }

  const tableHtml = `
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Gender</th>
          <th>City</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        ${students.map((student, index) => `
          <tr id="row-${index}">
            <td>${student.name}</td>
            <td>${student.gender}</td>
            <td>${student.city}</td>
            <td>
              <a href="#" onclick="updateStudent(${index})">Update</a>
              <a href="#" onclick="deleteStudent(${index})">Delete</a>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;

  studentDataContainer.innerHTML = tableHtml;
}

function updateStudent(index) {
  const selectedRow = document.getElementById(`row-${index}`);
  const name = selectedRow.cells[0].innerText;
  const gender = selectedRow.cells[1].innerText;
  const city = selectedRow.cells[2].innerText;

  const formHtml = `
    <form onsubmit="return submitForm(${index})">
      <label for="name">Name:</label>
      <input type="text" id="name" value="${name}">
      <br>
      <label for="gender">Gender:</label>
      <input type="text" id="gender" value="${gender}">
      <br>
      <label for="city">City:</label>
      <input type="text" id="city" value="${city}">
      <br>
      <button type="submit">Submit</button>
    </form>
  `;

  studentFormContainer.innerHTML = formHtml;
}

function deleteStudent(index) {
  const selectedRow = document.getElementById(`row-${index}`);
  selectedRow.remove();
}

function submitForm(index) {
  const name = document.getElementById('name').value;
  const gender = document.getElementById('gender').value;
  const city = document.getElementById('city').value;

  const updatedDataHtml = `
    <table>
      <thead>
        <tr>
          <th>Attribute Name</th>
          <th>Attribute Value</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Name</td>
          <td>${name}</td>
        </tr>
        <tr>
          <td>Gender</td>
          <td>${gender}</td>
        </tr>
        <tr>
          <td>City</td>
          <td>${city}</td>
        </tr>
      </tbody>
    </table>
  `;

  updatedDataContainer.innerHTML = updatedDataHtml;
  return false; // Prevent form submission
}
