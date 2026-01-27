import LanguageToggle from "../Components/Common/LanguageToggle";
import FileUpload from "../Components/Upload/FileUpload";
function Home(){
    return(
        <div className ="container">
            <LanguageToggle />
            <h1>Legal Easy AI</h1>

            <p>Upload legal documnets and understands them easily in Hindi and English </p>

            <FileUpload />
        </div>

    );
}

export default Home;