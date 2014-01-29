/**
 * Created by mzalota on 1/27/14.
 */

(function($) {
    $(document).ready(function() {
        //console.log($.fn.jquery);
         $(".maxtest").live('click', function(e) {
            //console.log("You clicked on a maxtest field");
            //$('[name="_selected_action"][value="54764"]').attr("checked",true);

             //Check box next to Event ID
             $(this).closest('tr').find('td:first').find('input').attr("checked",true);

             //Check the box with instructor ID
             $(this).parent('td').find('input:first').attr("checked",true);

             //Select action to be "link_to_instructor
             $('[name="action"] option[value="link_to_instructor"]').attr("selected","selected");


             //$(this)..parents("tr").find('td:first').find('input').attr("checked",true);

             $(this).parents("form").submit();
        });
    });
}(django.jQuery));
