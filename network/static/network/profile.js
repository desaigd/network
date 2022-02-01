
            
    function editpost(num) {
        var editview = document.querySelector(`#edit-view-${num}`);
        var normalview = document.querySelector(`#normal-view-${num}`);
        var savebutton = document.querySelector(`#save-${num}`);
        var content = document.querySelector(`#edit-text-${num}`); 
                
            normalview.style.display = 'none';
            editview.style.display = 'block';
                savebutton.addEventListener("click", () => { 
                    fetch('/edit/' + num, {
                        method: 'PUT',
                        body: JSON.stringify({
                        content: content.value
                        })
                    })
                    editview.style.display = 'none';
                    normalview.innerHTML = content.value;
                    normalview.style.display = 'block';
                });
        }
    
            
    function likepost(num) {
        var like = document.querySelector(`#like-${num}`);
        var unlike = document.querySelector(`#unlike-${num}`);
                
            like.addEventListener("click", () => { 
                fetch('/likepst/' + num, {
                    method: 'PUT',
                    body: JSON.stringify({
                    content: 'addlike'
                    })
                })
            });
                unlike.style.display = "block";
                like.style.display = "none";       
        } 

            
    function unlikepost(num) {
        var like = document.querySelector(`#like-${num}`);
        var unlike = document.querySelector(`#unlike-${num}`);
           
            unlike.addEventListener("click", () => {
                fetch('/likepst/' + num, {
                    method: 'PUT',
                    body: JSON.stringify({
                    content: 'unlike'
                    })
                })      
            });   
                like.style.display = "block";
                unlike.style.display = "none";
        }
            
            

       
        
         



         
        