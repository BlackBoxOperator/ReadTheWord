echo "SRC_DIR=data"

for dir in train validation test;do
  for subdir in `ls $dir`;do
    echo "mkdir -p $dir/$subdir/"
  done
done

for dir in train validation test;do
  for subdir in `ls $dir`;do
    for img in `ls $dir/$subdir`;do
      echo "ln -s \$SRC_DIR/$img $dir/$subdir/$img"
    done
  done
done
