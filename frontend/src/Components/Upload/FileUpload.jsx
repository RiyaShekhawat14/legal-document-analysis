
function FileUpload() {
    
    const handleFileChange = (event) =>{
        const file =event.target.files[0];
        console.log(file);
    };

    return (
        <div className="upload-box">
            <p>Select a legal document (PDF / DOC / TXT)</p>

            <input type="file" onChange={handleFileChange} />

            <button className="btn-primary mt-20">
                Analyze Document
            </button>
        </div>
    );
}

export default FileUpload;
