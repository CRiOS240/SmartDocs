import React, { useEffect, useRef, useState } from "react";
import Quill from "quill";
import "quill/dist/quill.snow.css"; 

function QuillEditor() {
  const editorRef = useRef(null); 
  const quillInstance = useRef(null); 
  const [content, setContent] = useState(""); 

  useEffect(() => {
    if (editorRef.current) {
      quillInstance.current = new Quill(editorRef.current, {
        theme: "snow", 
        modules: {
          toolbar:  [
            ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
            ['blockquote', 'code-block'],
            ['link', 'image', 'video', 'formula'],
          
            [{ 'header': 1 }, { 'header': 2 }],               // custom button values
            [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
            [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
            [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
            [{ 'direction': 'rtl' }],                         // text direction
          
            [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
          
            [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
            [{ 'font': [] }],
            [{ 'align': [] }],
          
            ['clean']                                         // remove formatting button
          ],
        },
      });

      quillInstance.current.on("text-change", () => {
        setContent(quillInstance.current.root.innerHTML);
      });
    }
  }, []);


  const handleSave = () => {
    console.log(content); 
  };

  const handleFileChange=()=>{
    
  }

  const handleUpload=()=>{
    
  }


  return (
    <div>
      <div ref={editorRef} style={{ height: "300px" }} />
      <button onClick={handleSave}>Save Content</button>
      <input type="file" onChange={handleFileChange}/>
      {/* <p>{fileName ?`Selected File: ${fileName}`:`No file selected.`}</p> */}
      <button onClick={handleUpload}></button>
    </div>
  );
}

export default QuillEditor;
