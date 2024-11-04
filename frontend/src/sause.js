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
          toolbar: [
            [{ header: [1, 2, false] }],
            ["bold", "italic", "underline"],
            ["link", "image"],
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



  return (
    <div>
      <div ref={editorRef} style={{ height: "300px" }} />
      <button onClick={handleSave}>Save Content</button>
      <input/>
    </div>
  );
}

export default QuillEditor;
