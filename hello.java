import java.sql.*;

public class CRUDOperations {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/your_database_name";
        String username = "root";
        String password = "password";

        try (Connection conn = DriverManager.getConnection(url, username, password)) {

            // Create - Insert data
            String insertQuery = "INSERT INTO your_table_name (name) VALUES (?)";
            try (PreparedStatement stmt = conn.prepareStatement(insertQuery)) {
                stmt.setString(1, "John Doe");
                int rowsInserted = stmt.executeUpdate();
                if (rowsInserted > 0) {
                    System.out.println("A new user was inserted successfully!");
                }
            }

            // Read - Retrieve data
            String selectQuery = "SELECT * FROM your_table_name";
            try (Statement stmt = conn.createStatement(); ResultSet rs = stmt.executeQuery(selectQuery)) {
                while (rs.next()) {
                    int id = rs.getInt("id");
                    String name = rs.getString("name");
                    System.out.println("ID: " + id + ", Name: " + name);
                }
            }

            // Update - Modify data
            String updateQuery = "UPDATE your_table_name SET name = ? WHERE id = ?";
            try (PreparedStatement stmt = conn.prepareStatement(updateQuery)) {
                stmt.setString(1, "Jane Smith");
                stmt.setInt(2, 1); // Assume we are updating the user with ID = 1
                int rowsUpdated = stmt.executeUpdate();
                if (rowsUpdated > 0) {
                    System.out.println("An existing user was updated successfully!");
                }
            }

            // Delete - Remove data
            String deleteQuery = "DELETE FROM your_table_name WHERE id = ?";
            try (PreparedStatement stmt = conn.prepareStatement(deleteQuery)) {
                stmt.setInt(1, 1); // Assume we are deleting the user with ID = 1
                int rowsDeleted = stmt.executeUpdate();
                if (rowsDeleted > 0) {
                    System.out.println("A user was deleted successfully!");
                }
            }

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
