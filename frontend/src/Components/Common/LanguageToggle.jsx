import { useContext} from "react";
import { LanguageContext } from "../../context/LanguageContext";

function LanguageToggle() {
    const { language, changeLanguage } = useContext(LanguageContext);

    return(
        <div>
            <button onClick ={() => changeLanguage('en')}
            className={language==="en"?"btn-primary":""}>
                English
            </button>

            <button onClick={()=> changeLanguage("hi")}
            style={{marginLeft:"10px"}}
             className={language==="hi"?"btn-primary":""}>
                Hindi
            </button>
            

        </div>
    );

}  
export default LanguageToggle;