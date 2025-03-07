document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("upload-form");
  
    form.addEventListener("submit", async function (event) {
      event.preventDefault();  // ✅ Prevent default form submission
      event.stopPropagation(); // ✅ Stop bubbling events
  
      const jobDesc = document.getElementById("job-desc").value;
      const resume = document.getElementById("resume").files[0];
  
      if (!resume) {
        alert("Please upload a resume file.");
        return;
      }
  
      // Check for valid file types (PDF or DOCX)
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (!validTypes.includes(resume.type)) {
        alert("Please upload a valid resume file (.pdf or .docx).");
        return;
      }
  
      // Show loading indicator
      const loadingElement = document.getElementById('loading');
      loadingElement.style.display = "block"; 
  
      try {
        const formData = new FormData();
        formData.append("job_desc", jobDesc);
        formData.append("resume", resume);
  
        const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });
  
        // Hide loading indicator
        loadingElement.style.display = "none"; 
  
        // Display match percentage result
        const matchPercentage = response.data.match;
        document.getElementById("match-percentage").innerHTML = `${matchPercentage}%`;
        document.getElementById("result-section").style.display = "block";  // ✅ Show result section
  
        console.log("✅ Match percentage received:", matchPercentage);
  
      } catch (error) {
        console.error("❌ Error submitting the form:", error);
        loadingElement.style.display = "none"; 
        alert("There was an error processing your request. Please try again.");
      }
    });
  });
  