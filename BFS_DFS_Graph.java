import java.util.*;

public class BFS_DFS_Graph {

    // ---------------- BFS ----------------
    public static List<String> bfs(Map<String, List<String>> graph, String start, String goal) {
        Queue<List<String>> queue = new LinkedList<>();
        Set<String> visited = new HashSet<>();

        queue.add(new ArrayList<>(Arrays.asList(start)));

        while (!queue.isEmpty()) {
            List<String> path = queue.poll();
            String node = path.get(path.size() - 1);

            if (!visited.contains(node)) {
                visited.add(node);

                if (node.equals(goal)) {
                    return path;
                }

                for (String neighbour : graph.get(node)) {
                    List<String> newPath = new ArrayList<>(path);
                    newPath.add(neighbour);
                    queue.add(newPath);
                }
            }
        }

        return null;
    }

    // ---------------- DFS ----------------
    public static List<String> dfs(Map<String, List<String>> graph, String start, String goal) {
        Stack<List<String>> stack = new Stack<>();
        Set<String> visited = new HashSet<>();

        stack.push(new ArrayList<>(Arrays.asList(start)));

        while (!stack.isEmpty()) {
            List<String> path = stack.pop();
            String node = path.get(path.size() - 1);

            if (!visited.contains(node)) {
                visited.add(node);

                if (node.equals(goal)) {
                    return path;
                }

                List<String> neighbours = new ArrayList<>(graph.get(node));
                Collections.sort(neighbours, Collections.reverseOrder());

                for (String neighbour : neighbours) {
                    List<String> newPath = new ArrayList<>(path);
                    newPath.add(neighbour);
                    stack.push(newPath);
                }
            }
        }

        return null;
    }

    // ---------------- Main Method ----------------
    public static void main(String[] args) {

        Map<String, List<String>> graph = new HashMap<>();

        graph.put("Alice", Arrays.asList("Charlie", "David"));
        graph.put("Charlie", Arrays.asList("Alice", "Emma"));
        graph.put("David", Arrays.asList("Alice", "Emma", "Fred"));
        graph.put("Emma", Arrays.asList("Bob", "Charlie", "David"));
        graph.put("Fred", Arrays.asList("Bob", "David"));
        graph.put("Bob", Arrays.asList("Emma", "Fred"));

        String source = "Alice";
        String goal = "Bob";

        List<String> bfsPath = bfs(graph, source, goal);
        List<String> dfsPath = dfs(graph, source, goal);

        System.out.println("BFS Path:");
        if (bfsPath != null) {
            System.out.println(String.join(" -> ", bfsPath));
        } else {
            System.out.println("No path found.");
        }

        System.out.println();

        System.out.println("DFS Path:");
        if (dfsPath != null) {
            System.out.println(String.join(" -> ", dfsPath));
        } else {
            System.out.println("No path found.");
        }
    }
}