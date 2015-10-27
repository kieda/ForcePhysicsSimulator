package edu.cmu.cs464.p3.util.quadtree;

public class Point<T> implements Comparable<Point> {

    private double x;
    private double y;
    private T opt_value;

    /**
     * Creates a new point object.
     *
     * @param {double} x The x-coordinate of the point.
     * @param {double} y The y-coordinate of the point.
     * @param {T} opt_value Optional value associated with the point.     
     */
    public Point(double x, double y, T opt_value) {
        this.x = x;
        this.y = y;
        this.opt_value = opt_value;
    }

    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }

    public T getValue() {
        return opt_value;
    }

    public void setValue(T opt_value) {
        this.opt_value = opt_value;
    }

    @Override
    public String toString() {
        return "(" + this.x + ", " + this.y + ")";
    }

    @Override
    public int compareTo(Point o) {
        Point tmp = (Point) o;
        if (this.x < tmp.x) {
            return -1;
        } else if (this.x > tmp.x) {
            return 1;
        } else {
            if (this.y < tmp.y) {
                return -1;
            } else if (this.y > tmp.y) {
                return 1;
            }
            return 0;
        }
    }
    public class PointImmutable{
        private PointImmutable(){}
        public double getX() {
            return x;
        }
            public double getY() {
            return y;
        }
        public T getValue() {
            return opt_value;
        }
        @Override
        public String toString() {
            return "(" + x + ", " + y + ")";
        }
    }
    private PointImmutable immutableVersion = null;
    
    /**
     * @return an immutable view of this point.
     */
    public PointImmutable getImmutable(){
        return immutableVersion == null ? immutableVersion = new PointImmutable() : immutableVersion;
    }
}
