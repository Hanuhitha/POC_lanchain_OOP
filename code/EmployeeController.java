import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EmployeeController {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @GetMapping("/employees")
    public String getEmployees() {
        String sql = "SELECT name, dob FROM Employee";
        return jdbcTemplate.queryForList(sql).toString();
    }
}
