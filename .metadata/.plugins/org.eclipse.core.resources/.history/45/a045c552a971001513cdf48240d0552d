package edu.cmu.cs464.p3.util.quadtree;

import java.util.AbstractMap;
import java.util.HashSet;
import java.util.Set;
import java.util.function.BiConsumer;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.stream.Collectors;
import javax.vecmath.Vector2d;

/**
 * Datastructure: A point Quad Tree for representing 2D data. Each
 * region has the same ratio as the bounds for the tree.
 * <p/>
 * The implementation currently requires pre-determined bounds for data as it
 * can not rebalance itself to that degree.
 * 
 * It's important to note that we use Vector2d as the key for this map, 
 * but the keys added/recieved from this map are all copied so there should
 * be no problems using this as a normal map (unless if there's some multi
 * threading funny business going on).
 */
public class QuadTree<T> implements Map<Vector2d, T>{
    private Node<T> root_;
    private int count_ = 0;

    /**
     * Constructs a new quad tree.
     *
     * @param {double} minX Minimum x-value that can be held in tree.
     * @param {double} minY Minimum y-value that can be held in tree.
     * @param {double} maxX Maximum x-value that can be held in tree.
     * @param {double} maxY Maximum y-value that can be held in tree.
     */
    public QuadTree(double minX, double minY, double maxX, double maxY) {
        this.root_ = new Node(minX, minY, maxX - minX, maxY - minY, null);
    }

    /**
     * Returns a reference to the tree's root node.  Callers shouldn't modify nodes,
     * directly.  This is a convenience for visualization and debugging purposes.
     *
     * @return {Node} The root node.
     */
    public Node<T> getRootNode() {
        return this.root_;
    }

    /**
     * Sets the value of an (x, y) point within the quad-tree.
     *
     * @param {double} x The x-coordinate.
     * @param {double} y The y-coordinate.
     * @param {Object} value The value associated with the point.
     */
    public void set(double x, double y, T value) {

        Node<T> root = this.root_;
        if (x < root.getX() || y < root.getY() || x > root.getX() + root.getW() || y > root.getY() + root.getH()) {
            throw new QuadTreeException("Out of bounds : (" + x + ", " + y + ")");
        }
        if (this.insert(root, new Point(x, y, value))) {
            this.count_++;
        }
    }

    /**
     * Gets the value of the point at (x, y) or null if the point is empty.
     *
     * @param {double} x The x-coordinate.
     * @param {double} y The y-coordinate.
     * @param {Object} opt_default The default value to return if the node doesn't
     *                 exist.
     * @return {*} The value of the node, the default value if the node
     *         doesn't exist, or undefined if the node doesn't exist and no default
     *         has been provided.
     */
    public T get(double x, double y, T opt_default) {
        Node<T> node = this.find(this.root_, x, y);
        return node != null ? node.getPoint().getValue() : opt_default;
    }

    /**
     * Removes a point from (x, y) if it exists.
     *
     * @param {double} x The x-coordinate.
     * @param {double} y The y-coordinate.
     * @return {Object} The value of the node that was removed, or null if the
     *         node doesn't exist.
     */
    public T remove(double x, double y) {
        Node<T> node = this.find(this.root_, x, y);
        if (node != null) {
            T value = node.getPoint().getValue();
            node.setPoint(null);
            node.setNodeType(NodeType.EMPTY);
            this.balance(node);
            this.count_--;
            return value;
        } else {
            return null;
        }
    }

    /**
     * Returns true if the point at (x, y) exists in the tree.
     *
     * @param {double} x The x-coordinate.
     * @param {double} y The y-coordinate.
     * @return {boolean} Whether the tree contains a point at (x, y).
     */
    public boolean contains(double x, double y) {
        return this.get(x, y, null) != null;
    }

    /**
     * @return {boolean} Whether the tree is empty.
     */
    public boolean isEmpty() {
        return this.root_.getNodeType() == NodeType.EMPTY;
    }

    /**
     * Removes all items from the tree.
     */
    public void clear() {
        this.root_.setNw(null);
        this.root_.setNe(null);
        this.root_.setSw(null);
        this.root_.setSe(null);
        this.root_.setNodeType(NodeType.EMPTY);
        this.root_.setPoint(null);
        this.count_ = 0;
    }

    /**
     * Returns a set containing the coordinates of each point stored in the tree.
     * @return coordinates.
     */
    public Set<Point<T>> getKeys() {
        final Set<Point<T>> arr = new HashSet<>();
        this.traverse(this.root_, (quadTree, node) -> 
                arr.add(node.getPoint())
            );
        return arr;
    }

    /**
     * Returns a set containing all values stored within the tree.
     * @return The values stored within the tree.
     */
    public Set<T> values() {
        final Set<T> arr = new HashSet<>();
        this.traverse(this.root_, (quadTree, node) -> 
                arr.add(node.getPoint().getValue())
            );

        return arr;
    }

    public Set<Point<T>> searchIntersect(final double xmin, final double ymin, final double xmax, final double ymax) {
        final Set<Point<T>> arr = new HashSet<>();
        this.navigate(this.root_, (quadTree, node) -> {
                Point pt = node.getPoint();
                if (pt.getX() < xmin || pt.getX() > xmax || pt.getY() < ymin || pt.getY() > ymax) {
                    // Definitely not within the polygon!
                } else {
                    arr.add(node.getPoint());
                }
            }, xmin, ymin, xmax, ymax);
        return arr;
    }

    public Set<Point<T>> searchWithin(final double xmin, final double ymin, final double xmax, final double ymax) {
        final Set<Point<T>> arr = new HashSet<>();
        this.navigate(this.root_, (quadTree, node) -> {
                Point pt = node.getPoint();
                if (pt.getX() > xmin && pt.getX() < xmax && pt.getY() > ymin && pt.getY() < ymax) {
                    arr.add(node.getPoint());
                }
            }, xmin, ymin, xmax, ymax);
        return arr;
    }

    public void navigate(Node<T> node, BiConsumer<QuadTree<T>, Node<T>> func, double xmin, double ymin, double xmax, double ymax) {
        switch (node.getNodeType()) {
            case LEAF:
                func.accept(this, node);
                break;

            case POINTER:
                if (intersects(xmin, ymax, xmax, ymin, node.getNe()))
                    this.navigate(node.getNe(), func, xmin, ymin, xmax, ymax);
                if (intersects(xmin, ymax, xmax, ymin, node.getSe()))
                    this.navigate(node.getSe(), func, xmin, ymin, xmax, ymax);
                if (intersects(xmin, ymax, xmax, ymin, node.getSw()))
                    this.navigate(node.getSw(), func, xmin, ymin, xmax, ymax);
                if (intersects(xmin, ymax, xmax, ymin, node.getNw()))
                    this.navigate(node.getNw(), func, xmin, ymin, xmax, ymax);
                break;
			default:
				break;
        }
    }

    private boolean intersects(double left, double bottom, double right, double top, Node<T> node) {
        return !(node.getX() > right ||
                (node.getX() + node.getW()) < left ||
                node.getY() > bottom ||
                (node.getY() + node.getH()) < top);
    }
    /**
     * Clones the quad-tree and returns the new instance.
     * @return {QuadTree} A clone of the tree.
     */
    public QuadTree<T> clone() {
        double x1 = this.root_.getX();
        double y1 = this.root_.getY();
        double x2 = x1 + this.root_.getW();
        double y2 = y1 + this.root_.getH();
        final QuadTree<T> clone = new QuadTree<>(x1, y1, x2, y2);
        // This is inefficient as the clone needs to recalculate the structure of the
        // tree, even though we know it already.  But this is easier and can be
        // optimized when/if needed.
        this.traverse(this.root_, (quadTree, node) ->
                clone.set(node.getPoint().getX(), node.getPoint().getY(), node.getPoint().getValue())
            );


        return clone;
    }

    /**
     * Traverses the tree depth-first, with quadrants being traversed in clockwise
     * order (NE, SE, SW, NW).  The provided function will be called for each
     * leaf node that is encountered.
     * @param {QuadTree.Node} node The current node.
     * @param {function(QuadTree.Node)} fn The function to call
     *     for each leaf node. This function takes the node as an argument, and its
     *     return value is irrelevant.
     * @private
     */
    public void traverse(Node<T> node, BiConsumer<QuadTree<T>, Node<T>> func) {
        switch (node.getNodeType()) {
            case LEAF:
                func.accept(this, node);
                break;

            case POINTER:
                this.traverse(node.getNe(), func);
                this.traverse(node.getSe(), func);
                this.traverse(node.getSw(), func);
                this.traverse(node.getNw(), func);
                break;
			default:
				break;
        }
    }
    
    /**
     * traverses and folds a value {@code K} across nodes that are children
     * of and are {@code node}. See {@code traverse} for the traversal order
     */
    public <K> K fold(Node<T> node, K val, BiFunction<Node<T>, K, K> func) {
        switch (node.getNodeType()) {
            case LEAF:
                return func.apply(node, val);

            case POINTER:
                val = fold(node.getNe(), val, func);
                val = fold(node.getSe(), val, func);
                val = fold(node.getSw(), val, func);
                return fold(node.getNw(), val, func);
            default:
                return val;
        }
    }

    /**
     * Finds a leaf node with the same (x, y) coordinates as the target point, or
     * null if no point exists.
     * @param {QuadTree.Node} node The node to search in.
     * @param {number} x The x-coordinate of the point to search for.
     * @param {number} y The y-coordinate of the point to search for.
     * @return {QuadTree.Node} The leaf node that matches the target,
     *     or null if it doesn't exist.
     * @private
     */
    public Node<T> find(Node<T> node, double x, double y) {
        Node<T> resposne = null;
        switch (node.getNodeType()) {
            case EMPTY:
                break;

            case LEAF:
                resposne = node.getPoint().getX() == x && node.getPoint().getY() == y ? node : null;
                break;

            case POINTER:
                resposne = this.find(this.getQuadrantForPoint(node, x, y), x, y);
                break;

            default:
                throw new QuadTreeException("Invalid nodeType");
        }
        return resposne;
    }

    /**
     * Inserts a point into the tree, updating the tree's structure if necessary.
     * @param {.QuadTree.Node} parent The parent to insert the point
     *     into.
     * @param {QuadTree.Point} point The point to insert.
     * @return {boolean} True if a new node was added to the tree; False if a node
     *     already existed with the correpsonding coordinates and had its value
     *     reset.
     * @private
     */
    private boolean insert(Node<T> parent, Point<T> point) {
        boolean result = false;
        switch (parent.getNodeType()) {
            case EMPTY:
                this.setPointForNode(parent, point);
                result = true;
                break;
            case LEAF:
                if (parent.getPoint().getX() == point.getX() && parent.getPoint().getY() == point.getY()) {
                    this.setPointForNode(parent, point);
                    result = false;
                } else {
                    this.split(parent);
                    result = this.insert(parent, point);
                }
                break;
            case POINTER:
                result = this.insert(
                        this.getQuadrantForPoint(parent, point.getX(), point.getY()), point);
                break;

            default:
                throw new QuadTreeException("Invalid nodeType in parent");
        }
        return result;
    }

    /**
     * Converts a leaf node to a pointer node and reinserts the node's point into
     * the correct child.
     * @param {QuadTree.Node} node The node to split.
     * @private
     */
    private void split(Node<T> node) {
        Point<T> oldPoint = node.getPoint();
        node.setPoint(null);

        node.setNodeType(NodeType.POINTER);

        double x = node.getX();
        double y = node.getY();
        double hw = node.getW() / 2;
        double hh = node.getH() / 2;

        node.setNw(new Node(x, y, hw, hh, node));
        node.setNe(new Node(x + hw, y, hw, hh, node));
        node.setSw(new Node(x, y + hh, hw, hh, node));
        node.setSe(new Node(x + hw, y + hh, hw, hh, node));

        this.insert(node, oldPoint);
    }

    /**
     * Attempts to balance a node. A node will need balancing if all its children
     * are empty or it contains just one leaf.
     * @param {QuadTree.Node} node The node to balance.
     * @private
     */
    private void balance(Node<T> node) {
        switch (node.getNodeType()) {
            case EMPTY:
            case LEAF:
                if (node.getParent() != null) {
                    this.balance(node.getParent());
                }
                break;

            case POINTER: {
                Node<T> nw = node.getNw();
                Node<T> ne = node.getNe();
                Node<T> sw = node.getSw();
                Node<T> se = node.getSe();
                Node<T> firstLeaf = null;

                // Look for the first non-empty child, if there is more than one then we
                // break as this node can't be balanced.
                if (nw.getNodeType() != NodeType.EMPTY) {
                    firstLeaf = nw;
                }
                if (ne.getNodeType() != NodeType.EMPTY) {
                    if (firstLeaf != null) {
                        break;
                    }
                    firstLeaf = ne;
                }
                if (sw.getNodeType() != NodeType.EMPTY) {
                    if (firstLeaf != null) {
                        break;
                    }
                    firstLeaf = sw;
                }
                if (se.getNodeType() != NodeType.EMPTY) {
                    if (firstLeaf != null) {
                        break;
                    }
                    firstLeaf = se;
                }

                if (firstLeaf == null) {
                    // All child nodes are empty: so make this node empty.
                    node.setNodeType(NodeType.EMPTY);
                    node.setNw(null);
                    node.setNe(null);
                    node.setSw(null);
                    node.setSe(null);

                } else if (firstLeaf.getNodeType() == NodeType.POINTER) {
                    // Only child was a pointer, therefore we can't rebalance.
                    break;

                } else {
                    // Only child was a leaf: so update node's point and make it a leaf.
                    node.setNodeType(NodeType.LEAF);
                    node.setNw(null);
                    node.setNe(null);
                    node.setSw(null);
                    node.setSe(null);
                    node.setPoint(firstLeaf.getPoint());
                }

                // Try and balance the parent as well.
                if (node.getParent() != null) {
                    this.balance(node.getParent());
                }
            }
            break;
        }
    }

    /**
     * Returns the child quadrant within a node that contains the given (x, y)
     * coordinate.
     * @param {QuadTree.Node} parent The node.
     * @param {number} x The x-coordinate to look for.
     * @param {number} y The y-coordinate to look for.
     * @return {QuadTree.Node} The child quadrant that contains the
     *     point.
     * @private
     */
    private Node<T> getQuadrantForPoint(Node<T> parent, double x, double y) {
        double mx = parent.getX() + parent.getW() / 2;
        double my = parent.getY() + parent.getH() / 2;
        if (x < mx) {
            return y < my ? parent.getNw() : parent.getSw();
        } else {
            return y < my ? parent.getNe() : parent.getSe();
        }
    }

    /**
     * Sets the point for a node, as long as the node is a leaf or empty.
     * @param {QuadTree.Node} node The node to set the point for.
     * @param {QuadTree.Point} point The point to set.
     * @private
     */
    private void setPointForNode(Node<T> node, Point<T> point) {
        if (node.getNodeType() == NodeType.POINTER) {
            throw new QuadTreeException("Can not set point for node of type POINTER");
        }
        node.setNodeType(NodeType.LEAF);
        node.setPoint(point);
    }

    @Override
    public int size() {
        return count_;
    }

    @Override
    public boolean containsKey(Object key) {
        if(key instanceof Vector2d){
            Vector2d pt = (Vector2d)key;
            return contains(pt.x, pt.y);
        }
        throw new IllegalArgumentException("expected key of type Vector2d, found " + key);
    }

    @Override
    public boolean containsValue(Object value) {
        return values().contains(value);
    }

    @Override
    public T get(Object key) {
        if(key instanceof Vector2d){
            Vector2d pt = (Vector2d)key;
            return get(pt.x, pt.y, null);
        }
        throw new IllegalArgumentException("expected key of type Vector2d, found " + key);
    }

    @Override
    public T put(Vector2d key, T value) {
        T re = get(key);
        set(key.x, key.y, value);
        return re;
    }

    @Override
    public T remove(Object key) {
        if(key instanceof Vector2d){
            Vector2d pt = (Vector2d)key;
            return remove(pt.x, pt.y);
        }
        throw new IllegalArgumentException("expected key of type Vector2d, found " + key);
    }

    @Override
    public void putAll(Map<? extends Vector2d, ? extends T> m) {
        m.forEach(this::put);
    }

    @Override
    public Set<Vector2d> keySet() {
        return getKeys().stream().map((pt)-> new Vector2d(pt.getX(), pt.getY())).collect(Collectors.toSet());
    }

    @Override
    public Set<Entry<Vector2d, T>> entrySet() {
        Set<Entry<Vector2d, T>> entries = new HashSet<>();
        traverse(root_, (quadTree, node) -> {
            Point<T> pt = node.getPoint();
            if(node != null)
                entries.add(new AbstractMap.SimpleImmutableEntry<>(
                    new Vector2d(pt.getX(), pt.getY()), pt.getValue()));
        });
        return entries;
    }
    
    public class QuadTreeImmutable {

        private QuadTreeImmutable() {}
        
        public Set<Entry<Vector2d, T>> entrySet() {
            return QuadTree.this.entrySet();
        }
        public int size() {
            return QuadTree.this.size();
        }

        public boolean containsKey(Vector2d key) {
            return QuadTree.this.containsKey(key);
        }

        public boolean containsValue(T value) {
            return QuadTree.this.containsValue(value);
        }

        public T get(Vector2d key) {
            return QuadTree.this.get(key);
        }

        public Node<T>.NodeImmutable find(Node<T>.NodeImmutable node, double x, double y) {
            Node<T> n = QuadTree.this.find(node.getPeer(), x, y);
            return n == null ? null : n.getImmutable();
        }

        public boolean contains(double x, double y) {
            return QuadTree.this.contains(x, y);
        }

        public Node.NodeImmutable getRootNode() {
            return QuadTree.this.getRootNode().getImmutable();
        }

        public T get(double x, double y, T opt_default) {
            return QuadTree.this.get(x, y, opt_default);
        }

        public boolean isEmpty() {
            return QuadTree.this.isEmpty();
        }

        private Set<Point<T>.PointImmutable> toImmutable(Set<Point<T>> vals){
            return vals.stream().map(Point::getImmutable).collect(Collectors.toSet());
        }
        
        public Set<Point<T>.PointImmutable> getKeys() {
            return toImmutable(QuadTree.this.getKeys());
        }
        public Set<T> values(){
            return QuadTree.this.values();
        }

        public Set<Point<T>.PointImmutable> searchIntersect(final double xmin, final double ymin, final double xmax, final double ymax) {
            return toImmutable(QuadTree.this.searchIntersect(xmin, ymin, xmax, ymax));
        }

        public Set<Point<T>.PointImmutable> searchWithin(final double xmin, final double ymin, final double xmax, final double ymax) {
            return toImmutable(QuadTree.this.searchWithin(xmin, ymin, xmax, ymax));
        }

        public void navigate(Node<T>.NodeImmutable node, BiConsumer<QuadTree<T>.QuadTreeImmutable, Node<T>.NodeImmutable> func, double xmin, double ymin, double xmax, double ymax) {
            QuadTree.this.navigate(node.getPeer(), (qt, n) -> func.accept(qt.getImmutable(), n.getImmutable()), xmin, ymin, xmax, ymax);
        }
        public void traverse(Node<T>.NodeImmutable node, BiConsumer<QuadTree<T>.QuadTreeImmutable, Node<T>.NodeImmutable> func) {
            QuadTree.this.traverse(node.getPeer(), (qt, n) -> func.accept(qt.getImmutable(), n.getImmutable()));
        }
        
        public <K> K fold(Node<T>.NodeImmutable node, K val, BiFunction<Node<T>.NodeImmutable, K, K> func) {
            return QuadTree.this.fold(node.getPeer(), val, (n, k) -> func.apply(n.getImmutable(), k));
        }
    }
    
    private QuadTreeImmutable immutableVersion = null;

    /**
     * @return an immutable view of this quadtree
     */
    public QuadTreeImmutable getImmutable() {
        return immutableVersion == null ? immutableVersion = new QuadTreeImmutable() : immutableVersion;
    }
    
}
