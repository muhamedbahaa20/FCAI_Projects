package com.example.xml_student;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.springframework.web.bind.annotation.*;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.*;

@RestController
@RequestMapping("/managment")

public class EmployeeManagementApp {

    private static final String FILE_PATH = "employees.json";
    private static final Gson gson = new Gson();



    private static List<Employee> loadEmployees() {
        try (FileReader fileReader = new FileReader(FILE_PATH)) {
            Type listType = new TypeToken<List<Employee>>() {}.getType();
            return gson.fromJson(fileReader, listType);
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    private static void saveEmployees(List<Employee> employees, boolean override) {
        List<Employee> existingEmployees;

        if (override) {
            existingEmployees = new ArrayList<>();
        } else {
            existingEmployees = loadEmployees();
        }
        // Append the new employees to the existing list
        existingEmployees.addAll(employees);

        try (FileWriter fileWriter = new FileWriter(FILE_PATH)) {
            gson.toJson(existingEmployees, fileWriter);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @PostMapping("/addNewEmployee")
    private static String addNewEmployee(@RequestBody List<Employee> employees) {

        saveEmployees(employees,false);
        return "employee/s added";

    }
    @GetMapping("/searchEmployee")
    private List<Employee> searchEmployee(@RequestParam(required = false) Integer id, @RequestParam(required = false) String designation) {
        List<Employee> existingEmployees = loadEmployees();
        List<Employee> searchList = new ArrayList<>();

        for (Employee employee : existingEmployees) {
            if ((id == null || employee.getEmployeeID() == id) &&
                    (designation == null || employee.getDesignation().equalsIgnoreCase(designation))) {
                searchList.add(employee);
            }
        }

        return searchList;
    }


    @DeleteMapping("/deleteEmployee")
    private  void deleteEmployee(@RequestParam Integer id) {
        List<Employee> existingEmployees = loadEmployees();

        existingEmployees.removeIf(employee -> employee.getEmployeeID() == id);
        saveEmployees(existingEmployees,true);
    }

    @PutMapping("/updateEmployeeDesignation")
    private  String updateEmployeeDesignation(@RequestParam Integer id, @RequestParam String designation) {
        List<Employee> existingEmployees = loadEmployees();

        for (Employee employee : existingEmployees) {
            if (employee.getEmployeeID() == id) {
                employee.setDesignation(designation);
                saveEmployees(existingEmployees,true);
                return "Employee designation updated successfully!";
            }
        }

        return "No matching employee found.";
    }

    @GetMapping("/retrieveExperts")
    private List<Employee> retrieveExperts(@RequestParam String language, @RequestParam Integer MinScore) {

        List<Employee> existingEmployees = loadEmployees();

        List<Employee> Experts = new ArrayList<>();

        // Retrieve employees who know the specified language with a score in the given range
        for (Employee employee : existingEmployees) {
            for (KnownLanguage knownLanguage : employee.getKnownLanguages()) {
                if (knownLanguage.getLanguageName().equalsIgnoreCase(language) &&
                        knownLanguage.getScoreOutof100() >= MinScore) {
                    Experts.add(employee);
                    break; // Skip checking other languages for this employee
                }
            }
        }


        Collections.sort(Experts, Comparator.comparingInt(Employee::getEmployeeID));

        // Print the result
        if (!Experts.isEmpty()) {
            return Experts;
        }

    return null;
}
}
